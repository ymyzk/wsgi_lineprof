from io import TextIOWrapper  # noqa: F401
import sys
from queue import Queue, Empty
from threading import Thread
from typing import Callable, Iterable, TextIO, Union  # noqa: F401

from wsgi_lineprof.profiler import LineProfiler
from wsgi_lineprof.stats import FilterType  # noqa: F401


def writer(stats_queue, stream):
    while True:
        try:
            stats = stats_queue.get(timeout=5)
            stats.write_text(stream)
        except Empty:
            continue


class LineProfilerMiddleware(object):
    def __init__(self,
                 app,  # type: Callable
                 stream=None,  # type: Union[TextIO, TextIOWrapper]
                 filters=tuple(),  # type: Iterable[FilterType]
                 async_write=False,  # type bool
                 ):
        # type: (...) -> None
        self.app = app
        self.stream = sys.stdout if stream is None else stream
        self.filters = filters
        self.write_stats = self._write

        if async_write:
            self.write_stats = self._write_request
            self.queue = Queue()  # type: Queue
            self.writer_thread = Thread(target=writer, args=(self.queue, self.stream))
            self.writer_thread.setDaemon(True)
            self.writer_thread.start()

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

    def _write(self, stats):
        stats.write_text(self.stream)

    def _write_request(self, stats):
        self.queue.put(stats)
