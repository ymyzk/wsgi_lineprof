import sys
from typing import (Any, Callable, Iterable, Optional,  # noqa: F401
                    TYPE_CHECKING)  # noqa: F401

from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType  # noqa: F401
from wsgi_lineprof.types import Stream  # noqa: F401
from wsgi_lineprof.writers import (AsyncWriter, BaseWriter,  # noqa: F401
                                   SyncWriter)  # noqa: F401


if TYPE_CHECKING:
    from wsgiref.types import (StartResponse, WSGIApplication,  # noqa: F401
                               WSGIEnvironment)  # noqa: F401


class LineProfilerMiddleware(object):
    def __init__(self,
                 app,  # type: WSGIApplication
                 stream=None,  # type: Optional[Stream]
                 filters=tuple(),  # type: Iterable[FilterType]
                 async_stream=False,  # type: bool
                 ):
        # type: (...) -> None
        self.app = app
        self.stream = sys.stdout if stream is None else stream  # type: Stream
        self.filters = filters
        if async_stream:
            self.writer = AsyncWriter(self.stream)  # type: BaseWriter
        else:
            self.writer = SyncWriter(self.stream)  # type: BaseWriter

    def __call__(self, env, start_response):
        # type: (WSGIEnvironment, StartResponse) -> Iterable[bytes]
        profiler = LineProfiler()

        profiler.enable()
        result = self.app(env, start_response)
        profiler.disable()

        stats = profiler.get_stats()

        for f in self.filters:
            stats = stats.filter(f)

        self.writer.write(stats)

        return result
