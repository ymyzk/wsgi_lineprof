import atexit
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
                 accumulate=False,  # type: bool
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
        self.profiler = LineProfiler()
        # Cannot use AsyncWriter with atexit
        if async_stream and not accumulate:
            self.writer = AsyncWriter(self.stream)  # type: BaseWriter
        else:
            self.writer = SyncWriter(self.stream)
        if accumulate:
            atexit.register(self._write_stats)

    def _write_stats(self):
        # type: () -> None
        stats = self.profiler.get_stats()
        for f in self.filters:
            stats = stats.filter(f)
        self.writer.write(stats)

    def __call__(self, env, start_response):
        # type: (WSGIEnvironment, StartResponse) -> Iterable[bytes]
        if not self.accumulate:
            self.profiler.reset()
        self.profiler.enable()
        result = self.app(env, start_response)
        self.profiler.disable()

        if not self.accumulate:
            self._write_stats()

        return result
