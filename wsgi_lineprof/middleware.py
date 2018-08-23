from io import TextIOWrapper  # noqa: F401
from queue import Queue
import sys
from threading import Thread
from typing import Any, Callable, Iterable, TextIO, Union  # noqa: F401

from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType, LineProfilerStats  # noqa: F401


class SyncWriter(object):
    def __init__(self,
                 stream,  # type: Union[TextIO, TextIOWrapper]
                 ):
        # type: (...) -> None
        self.stream = stream

    def write(self, stats):
        # type: (LineProfilerStats) -> None
        stats.write_text(self.stream)


class AsyncWriter(object):
    def __init__(self,
                 stream,  # type: Union[TextIO, TextIOWrapper]
                 ):
        # type: (...) -> None
        self.stream = stream
        self.queue = Queue()  # type: Queue
        self.writer_thread = Thread(target=self._write)
        self.writer_thread.setDaemon(True)
        self.writer_thread.start()

    def write(self, stats):
        # type: (LineProfilerStats) -> None
        self.queue.put(stats)

    def _write(self):
        # type: () -> None
        while True:
            stats = self.queue.get()
            stats.write_text(self.stream)


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
