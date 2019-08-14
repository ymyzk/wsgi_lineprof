from abc import ABCMeta, abstractmethod
from six import add_metaclass
from six.moves.queue import Queue
from threading import Thread
from typing import Any, Tuple

from wsgi_lineprof.stats import LineProfilerStats
from wsgi_lineprof.types import Stream


@add_metaclass(ABCMeta)
class BaseWriter(object):
    @abstractmethod
    def __init__(self,
                 stream,  # type: Stream
                 *kwargs  # type: Any
                 ):
        # type: (...) -> None
        return

    @abstractmethod
    def write(self, stats, color=False):
        # type: (LineProfilerStats, bool) -> None
        return


class SyncWriter(BaseWriter):
    def __init__(self,
                 stream,  # type: Stream
                 ):
        # type: (...) -> None
        self.stream = stream

    def write(self, stats, color=False):
        # type: (LineProfilerStats, bool) -> None
        stats.write_text(self.stream, color=color)


class AsyncWriter(BaseWriter):
    def __init__(self,
                 stream,  # type: Stream
                 ):
        # type: (...) -> None
        self.stream = stream
        self.queue = Queue()  # type: Queue[Tuple[LineProfilerStats, bool]]
        self.writer_thread = Thread(target=self._write)
        self.writer_thread.setDaemon(True)
        self.writer_thread.start()

    def write(self, stats, color=False):
        # type: (LineProfilerStats, bool) -> None
        self.queue.put((stats, color))

    def _write(self):
        # type: () -> None
        while True:
            stats, color = self.queue.get()
            stats.write_text(self.stream, color=color)
