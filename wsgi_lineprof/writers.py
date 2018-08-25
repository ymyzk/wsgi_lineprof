from abc import ABCMeta, abstractmethod
from six import add_metaclass
from six.moves import queue
from threading import Thread
from typing import Any  # noqa: F401

from wsgi_lineprof.stats import LineProfilerStats  # noqa: F401
from wsgi_lineprof.types import Stream  # noqa: F401


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
    def write(self, stats):
        # type: (LineProfilerStats) -> None
        return


class SyncWriter(BaseWriter):
    def __init__(self,
                 stream,  # type: Stream
                 ):
        # type: (...) -> None
        self.stream = stream

    def write(self, stats):
        # type: (LineProfilerStats) -> None
        stats.write_text(self.stream)


class AsyncWriter(BaseWriter):
    def __init__(self,
                 stream,  # type: Stream
                 ):
        # type: (...) -> None
        self.stream = stream
        self.queue = queue.Queue()  # type: queue.Queue
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
