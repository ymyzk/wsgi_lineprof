from abc import ABCMeta, abstractmethod
from six import add_metaclass
from six.moves.queue import Queue
from threading import Thread
from typing import Any

from wsgi_lineprof.formatter import BaseFormatter
from wsgi_lineprof.stats import LineProfilerStats
from wsgi_lineprof.types import Stream


@add_metaclass(ABCMeta)
class BaseStreamWriter(object):
    def __init__(self,
                 stream,  # type: Stream
                 formatter,  # type: BaseFormatter
                 *kwargs  # type: Any
                 ):
        # type: (...) -> None
        self.stream = stream
        self.formatter = formatter

    @abstractmethod
    def write(self, stats):
        # type: (LineProfilerStats) -> None
        return


class SyncStreamWriter(BaseStreamWriter):
    def write(self, stats):
        # type: (LineProfilerStats) -> None
        self.formatter.format_stats(stats, self.stream)


class AsyncStreamWriter(BaseStreamWriter):
    def __init__(self,
                 stream,  # type: Stream
                 formatter  # type: BaseFormatter
                 ):
        # type: (...) -> None
        super(AsyncStreamWriter, self).__init__(stream, formatter)
        self.queue = Queue()  # type: Queue[LineProfilerStats]
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
            self.formatter.format_stats(stats, self.stream)
