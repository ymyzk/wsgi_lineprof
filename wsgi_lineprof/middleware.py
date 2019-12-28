from __future__ import absolute_import
import atexit
from six.moves import reduce
import sys
import threading
from types import CodeType
from typing import Any, Dict, Iterable, List, Optional, Type, TYPE_CHECKING

from wsgi_lineprof.extensions import LineTiming
from wsgi_lineprof.formatter import TextFormatter
from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType, LineProfilerStats, LineProfilerStat
from wsgi_lineprof.types import Stream
from wsgi_lineprof.writers import AsyncWriter, BaseWriter, SyncWriter


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
        self.results = []  # type: List[Dict[CodeType, Dict[int, LineTiming]]]
        # Enable colorization only for stdout/stderr
        color = color and stream in {sys.stdout, sys.stderr}
        formatter = TextFormatter(color=color)
        # A lock to avoid multiple threads try to write the result at the same time
        self.writer_lock = threading.Lock()
        # Cannot use AsyncWriter with atexit
        if async_stream and not accumulate:
            self.writer = AsyncWriter(stream, formatter)  # type: BaseWriter
        else:
            self.writer = SyncWriter(stream, formatter)
        if accumulate:
            atexit.register(self._write_result_at_exit)

    def _write_result_to_stream(self, result):
        # type: (Dict[CodeType, Dict[int, LineTiming]]) -> None
        stats = LineProfilerStats([LineProfilerStat(c, t) for c, t in result.items()],
                                  self.profiler_class.get_unit())
        for f in self.filters:
            stats = stats.filter(f)
        with self.writer_lock:
            self.writer.write(stats)

    def _write_result_at_exit(self):
        # type: () -> None
        """Write profiling results to the stream when exiting

        This method must be registered by only one thread.
        """
        result = {}  # type: Dict[CodeType, Dict[int, LineTiming]]
        result = reduce(_merge_results, self.results, {})
        self._write_result_to_stream(result)

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
        profiler = self.profiler_class()
        profiler.enable()
        try:
            response = self.app(env, start_response)
        finally:
            profiler.disable()

        if self.accumulate:
            # list.append is a thread safe operation
            self.results.append(profiler.results)
        else:
            self._write_result_to_stream(profiler.results)

        return response


def _merge_timings(a, b):
    # type: (Dict[int, LineTiming], Dict[int, LineTiming]) -> Dict[int, LineTiming]
    for line, timing in b.items():
        if line in a:
            a[line] += timing
        else:
            a[line] = timing
    return a


def _merge_results(
        a,  # type: Dict[CodeType, Dict[int, LineTiming]]
        b,  # type: Dict[CodeType, Dict[int, LineTiming]]
):
    # type: (...) -> Dict[CodeType, Dict[int, LineTiming]]
    for code, timings in b.items():
        if code in a:
            a[code] = _merge_timings(a[code], timings)
        else:
            a[code] = timings
    return a
