from io import TextIOWrapper  # noqa: F401
import sys
from typing import Callable, Iterable, TextIO, Union, List  # noqa: F401

from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType, LineProfilerStats  # noqa: F401


class LineProfilerMiddleware(object):
    def __init__(self,
                 app,  # type: Callable
                 stream=None,  # type: Union[TextIO, TextIOWrapper]
                 filters=tuple(),  # type: Iterable[FilterType]
                 buffer_size=0  # type: int
                 ):
        # type: (...) -> None
        self.app = app
        self.stream = sys.stdout if stream is None else stream
        self.filters = filters
        self.buffer_size = buffer_size
        self._stats_buffer = []  # type: List[LineProfilerStats]
        self.write_stats = self._write_stats
        # if buffer enable, switch write stats function
        if self.buffer_size > 0:
            self.write_stats = self._write_stats_with_buffer

    def __call__(self, env, start_response):
        profiler = LineProfiler()

        profiler.enable()
        result = self.app(env, start_response)
        profiler.disable()

        stats = profiler.get_stats()

        for f in self.filters:
            stats = stats.filter(f)
        self.write_stats(stats)

        return result

    def _write_stats(self, stats):
        stats.write_text(self.stream)

    def _write_stats_with_buffer(self, stats):
        self._stats_buffer.append(stats)
        if len(self._stats_buffer) > self.buffer_size:
            [s.write_text(self.stream) for s in self._stats_buffer]
            self._stats_buffer = []
