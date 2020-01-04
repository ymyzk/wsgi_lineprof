from abc import ABCMeta, abstractmethod
from six import add_metaclass
from six.moves.queue import Queue
from threading import Thread
from typing import Any, Optional

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
        # None in the queue is a special message to stop the writer thread
        self.queue = Queue()  # type: Queue[Optional[LineProfilerStats]]
        self.writer_thread = Thread(target=self._write)
        self.writer_thread.setDaemon(True)
        self.writer_thread.start()

    def write(self, stats):
        # type: (LineProfilerStats) -> None
        # Avoid accidentally stopping the writer thread by writing None
        if stats is None:
            return
        self.queue.put(stats)

    def _write(self):
        # type: () -> None
        """Method to run in the writer thread"""
        while True:
            stats = self.queue.get()
            if stats is None:
                return
            self.formatter.format_stats(stats, self.stream)

    def _join(self):
        # type: () -> None
        """Utility method to stop the writer thread

        Mainly for testing.
        """
        self.queue.put(None)
        self.writer_thread.join()
