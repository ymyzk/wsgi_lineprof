from io import TextIOWrapper  # noqa: F401
import sys
from typing import Any, Callable, Iterable, TextIO, Union  # noqa: F401

from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType  # noqa: F401
from wsgi_lineprof.writers import AsyncWriter, SyncWriter


class LineProfilerMiddleware(object):
    def __init__(self,
                 app,  # type: Callable
                 stream=None,  # type: Union[TextIO, TextIOWrapper]
                 filters=tuple(),  # type: Iterable[FilterType]
                 async_stream=False,  # type: bool
                 ):
        # type: (...) -> None
        self.app = app
        self.stream = sys.stdout if stream is None else stream
        self.filters = filters
        if async_stream:
            self.writer = AsyncWriter(self.stream)  # type: Any
        else:
            self.writer = SyncWriter(self.stream)

    def __call__(self, env, start_response):
        profiler = LineProfiler()

        profiler.enable()
        result = self.app(env, start_response)
        profiler.disable()

        stats = profiler.get_stats()

        for f in self.filters:
            stats = stats.filter(f)

        self.writer.write(stats)

        return result
