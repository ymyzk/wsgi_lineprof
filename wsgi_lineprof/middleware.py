import sys
from typing import Any, Callable, Iterable  # noqa: F401

from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType  # noqa: F401
from wsgi_lineprof.types import Stream  # noqa: F401
from wsgi_lineprof.writers import AsyncWriter, SyncWriter


class LineProfilerMiddleware(object):
    def __init__(self,
                 app,  # type: Callable
                 stream=None,  # type: Stream
                 filters=tuple(),  # type: Iterable[FilterType]
                 async_stream=False,  # type: bool
                 ):
        # type: (...) -> None
        self.app = app
        self.stream = sys.stdout if stream is None else stream
        self.filters = filters
        # TODO: "type: ignore" is for supressing mypy errors
        if async_stream:
            self.writer = AsyncWriter(self.stream)  # type: ignore
        else:
            self.writer = SyncWriter(self.stream)  # type: ignore

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
