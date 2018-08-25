from abc import ABCMeta, abstractmethod
from io import TextIOWrapper  # noqa: F401
from six import add_metaclass
from six.moves import queue
from threading import Thread
from typing import Any, TextIO, Union  # noqa: F401

from wsgi_lineprof.stats import LineProfilerStats  # noqa: F401


@add_metaclass(ABCMeta)
class BaseWriter(object):
    @abstractmethod
    def __init__(self,
                 stream,  # type: Union[TextIO, TextIOWrapper]
                 *kwargs  # type: Any
                 ):
        # type: (...) -> None
        return

    @abstractmethod
    def write(self, stats):
        return


class SyncWriter(BaseWriter):
    def __init__(self,
                 stream,  # type: Union[TextIO, TextIOWrapper]
                 ):
        # type: (...) -> None
        self.stream = stream

    def write(self, stats):
        # type: (LineProfilerStats) -> None
        stats.write_text(self.stream)


class AsyncWriter(BaseWriter):
    def __init__(self,
                 stream,  # type: Union[TextIO, TextIOWrapper]
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
