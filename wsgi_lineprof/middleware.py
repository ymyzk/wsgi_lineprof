import atexit
import sys
from six.moves import reduce
from types import CodeType
from typing import Any, Iterable, List, Optional, TYPE_CHECKING, Dict

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
                 ):
        # type: (...) -> None
        self.app = app
        # A hack to suppress unexpected mypy error on Python 2
        # error: Incompatible types in assignment
        # (expression has type "object", variable has type "TextIO")
        stdout = sys.stdout  # type: Any
        self.stream = stdout if stream is None else stream  # type: Stream
        self.filters = filters
        self.accumulate = accumulate
        self.results = []  # type: List[Dict[CodeType, Dict[int, LineTiming]]]
        # Enable colorization only for stdout/stderr
        color = color and self.stream in {sys.stdout, sys.stderr}
        self.formatter = TextFormatter(color=color)
        # Cannot use AsyncWriter with atexit
        if async_stream and not accumulate:
            self.writer = AsyncWriter(self.stream,
                                      self.formatter)  # type: BaseWriter
        else:
            self.writer = SyncWriter(self.stream, self.formatter)
        if accumulate:
            atexit.register(self._write_stats)

    def _write_stats(self):
        # type: () -> None
        result = reduce(_merge_results, self.results, initial={})
        stats = LineProfilerStats(
            [LineProfilerStat(c, t) for c, t in result.items()],
            LineProfiler.get_unit())
        for f in self.filters:
            stats = stats.filter(f)
        self.writer.write(stats)

    def __call__(self, env, start_response):
        # type: (WSGIEnvironment, StartResponse) -> Iterable[bytes]
        profiler = LineProfiler()
        profiler.enable()
        response = self.app(env, start_response)
        profiler.disable()

        if self.accumulate:
            self.results.append(profiler.results)
        else:
            self.results = [profiler.results]
            self._write_stats()

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
