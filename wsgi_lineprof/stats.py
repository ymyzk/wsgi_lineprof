import inspect
import itertools
import linecache
from os import path
from typing import Any, Callable, Dict, Iterable, Sequence, Union  # noqa: F401

from wsgi_lineprof.extensions import (  # noqa: F401
    LineProfiler as _LineProfiler, LineTiming
)
from wsgi_lineprof.filters import BaseFilter
from wsgi_lineprof.types import Stream  # noqa: F401


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
        total_time = sum(t.total_time for t in timings.values())
        self.total_time = total_time * _LineProfiler.get_unit()

    def write_text(self, stream):
        # type: (Stream) -> None
        stream.write("File: %s\n" % self.filename)
        stream.write("Name: %s\n" % self.name)
        stream.write("Total time: %g [sec]\n" % self.total_time)
        if not path.exists(self.filename):
            # e.g., filename is <frozen importlib._bootstrap>
            stream.write("WARNING: Cannot fild a file\n")
            return

        linecache.clearcache()
        lines = linecache.getlines(self.filename)  # type: Sequence[str]
        if self.name != "<module>":
            lines = inspect.getblock(lines[self.firstlineno - 1:])

        template = '%6s %9s %12s  %-s'
        header = template % ("Line", "Hits", "Time", "Code")
        stream.write(header)
        stream.write("\n")
        stream.write("=" * len(header))
        stream.write("\n")

        d = {}  # type: Dict[int, Dict[str, Any]]
        for i, code in zip(itertools.count(self.firstlineno), lines):
            timing = self.timings.get(i)
            if timing is None:
                d[i] = {
                    "hits": "",
                    "time": "",
                    "code": code
                }
            else:
                d[i] = {
                    "hits": timing.n_hits,
                    "time": timing.total_time,
                    "code": code
                }
        for i in sorted(d.keys()):
            r = d[i]
            stream.write(template % (i, r["hits"], r["time"], r["code"]))
        stream.write("\n")


CallableFilterType = Callable[[Iterable[LineProfilerStat]],
                              Iterable[LineProfilerStat]]
FilterType = Union[CallableFilterType, BaseFilter]


class LineProfilerStats(object):
    def __init__(self, stats):
        # type: (Iterable[LineProfilerStat]) -> None
        self.stats = stats

    def write_text(self, stream):
        # type: (Stream) -> None
        stream.write("Time unit: %s [sec]\n\n" % _LineProfiler.get_unit())
        for stat in self.stats:
            stat.write_text(stream)

    def filter(self, f):
        # type: (FilterType) -> LineProfilerStats
        if isinstance(f, BaseFilter):
            return LineProfilerStats(f.filter(self.stats))
        else:
            return LineProfilerStats(f(self.stats))
