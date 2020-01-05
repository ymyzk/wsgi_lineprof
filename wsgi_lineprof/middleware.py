from __future__ import absolute_import
import atexit
from collections import OrderedDict
from datetime import datetime
from operator import itemgetter
from six.moves import reduce
import sys
import threading
from typing import Any, Dict, Iterable, Optional, Type, TYPE_CHECKING
import uuid

from pytz import utc

from wsgi_lineprof.app import ResultsApp
from wsgi_lineprof.formatter import TextFormatter
from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType, LineProfilerStats
from wsgi_lineprof.types import CodeTiming, Measurement, RequestMeasurement, Stream
from wsgi_lineprof.writers import AsyncStreamWriter, BaseStreamWriter, SyncStreamWriter


if TYPE_CHECKING:
    from wsgiref.types import StartResponse, WSGIApplication, WSGIEnvironment


class LineProfilerMiddleware(object):
    def __init__(self,
                 app,  # type: WSGIApplication
                 stream=None,  # type: Optional[Stream]
                 filters=tuple(),  # type: Iterable[FilterType]
                 async_stream=False,  # type: bool
                 accumulate=False,  # type: bool
                 color=True,  # type: bool
                 profiler_class=LineProfiler,  # type: Type[LineProfiler]
                 endpoint="/wsgi_lineprof/",  # type: str
                 ):
        # type: (...) -> None
        self.app = app
        self.profiler_class = profiler_class
        # A hack to suppress unexpected mypy error on Python 2
        # error: Incompatible types in assignment
        # (expression has type "object", variable has type "TextIO")
        stdout = sys.stdout  # type: Any
        stream = stdout if stream is None else stream
        self.filters = filters
        self.accumulate = accumulate
        # TODO: Use typing.OrderedDict
        self.results = OrderedDict()  # type: Dict[uuid.UUID, RequestMeasurement]
        # Enable colorization only for stdout/stderr
        color = color and stream in {sys.stdout, sys.stderr}
        formatter = TextFormatter(color=color)
        # A lock to avoid multiple threads try to write the result at the same time
        self.writer_lock = threading.Lock()
        # Cannot use AsyncWriter with atexit
        if async_stream and not accumulate:
            self.writer = AsyncStreamWriter(stream, formatter)  # type: BaseStreamWriter
        else:
            self.writer = SyncStreamWriter(stream, formatter)
        if accumulate:
            atexit.register(self._write_result_at_exit)

        self.results_app = ResultsApp(
            endpoint=endpoint,
            results=self.results,
            filters=self.filters,
        )

    def _write_result_to_stream(self, measurement):
        # type: (Measurement) -> None
        stats = LineProfilerStats.from_measurement_and_unit(
            measurement, self.profiler_class.get_unit())
        for f in self.filters:
            stats = stats.filter(f)
        with self.writer_lock:
            self.writer.write(stats)

    def _write_result_at_exit(self):
        # type: () -> None
        """Write profiling results to the stream when exiting

        This method must be registered by only one thread.
        """
        measurement = reduce(
            _merge_results,
            map(itemgetter("results"), self.results.values()),
            {})  # type: Measurement
        self._write_result_to_stream(measurement)

    def __call__(self, env, start_response):
        # type: (WSGIEnvironment, StartResponse) -> Iterable[bytes]
        """Wrap an WSGI app with profiler

        Note that this thread may be called by multiple different threads.
        LineProfiler is not a thread-safe class.

        1. Create a profiler for this thread
        2. Run an WSGI application with profiling enabled
        3. Store the result of profiling or write it immediately
        4. Return the response from the WSGI application
        """
        if self.results_app.should_handle_request(env):
            return self.results_app(env, start_response)

        profiler = self.profiler_class()
        started_at = datetime.now(tz=utc)
        relative_start = profiler.get_timer()
        try:
            profiler.enable()
            response = self.app(env, start_response)
        finally:
            profiler.disable()
            unit = profiler.get_unit()
            elapsed = (profiler.get_timer() - relative_start) * unit

        request_id = uuid.uuid4()
        self.results[request_id] = {
            "id": request_id,
            "started_at": started_at,
            "elapsed": elapsed,
            "unit": unit,
            "results": profiler.results,
            "request_method": env["REQUEST_METHOD"],
            "path_info": env["PATH_INFO"],
            "query_string": env["QUERY_STRING"],
        }

        if not self.accumulate:
            self._write_result_to_stream(profiler.results)

        return response


def _merge_timings(a, b):
    # type: (CodeTiming, CodeTiming) -> CodeTiming
    for line, timing in b.items():
        if line in a:
            a[line] += timing
        else:
            a[line] = timing
    return a


def _merge_results(a, b):
    # type: (Measurement, Measurement) -> Measurement
    for code, timings in b.items():
        if code in a:
            a[code] = _merge_timings(a[code], timings)
        else:
            a[code] = timings
    return a
