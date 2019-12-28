from __future__ import absolute_import
from types import CodeType
from typing import Callable, Dict, Iterable, Union

from wsgi_lineprof.extensions import LineTiming
from wsgi_lineprof.filters import BaseFilter


class LineProfilerStat(object):
    def __init__(self,
                 code,  # type: CodeType
                 timings  # type: Dict[int, LineTiming]
                 ):
        # type: (...) -> None
        self.code = code
        self.timings = timings
        self.total_time = sum(t.total_time for t in timings.values())

    @property
    def filename(self):
        # type: () -> str
        # TODO: Improve how to handle empty filename
        filename = self.code.co_filename
        return filename if filename is not None else ""

    @property
    def name(self):
        # type: () -> str
        return self.code.co_name

    @property
    def firstlineno(self):
        # type: () -> int
        return self.code.co_firstlineno


CallableFilterType = Callable[[Iterable[LineProfilerStat]],
                              Iterable[LineProfilerStat]]
FilterType = Union[CallableFilterType, BaseFilter]


class LineProfilerStats(object):
    def __init__(self, stats, unit):
        # type: (Iterable[LineProfilerStat], float) -> None
        self.stats = stats
        self.unit = unit  # seconds/hit

    def filter(self, f):
        # type: (FilterType) -> LineProfilerStats
        if isinstance(f, BaseFilter):
            return LineProfilerStats(f.filter(self.stats), self.unit)
        else:
            return LineProfilerStats(f(self.stats), self.unit)
