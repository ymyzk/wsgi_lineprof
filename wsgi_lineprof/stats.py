from __future__ import division
from typing import Callable, Dict, Iterable, Union

from wsgi_lineprof.extensions import LineTiming
from wsgi_lineprof.filters import BaseFilter


class LineProfilerStat(object):
    def __init__(self,
                 filename,  # type: str
                 name,  # type: str
                 firstlineno,  # type: int
                 timings  # type: Dict[int, LineTiming]
                 ):
        # type: (...) -> None
        self.filename = filename
        self.name = name
        self.firstlineno = firstlineno
        self.timings = timings
        self.total_time = sum(t.total_time for t in timings.values())


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
