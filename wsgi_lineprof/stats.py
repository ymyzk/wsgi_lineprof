import inspect
from io import TextIOWrapper  # noqa: F401
import itertools
import linecache
from os import path
from typing import Callable, Iterable, TextIO, Union  # noqa: F401

from _wsgi_lineprof import LineProfiler as _LineProfiler
from wsgi_lineprof.filters import BaseFilter


class LineProfilerStat(object):
    def __init__(self, filename, name, firstlineno, timings):
        self.filename = filename
        self.name = name
        self.firstlineno = firstlineno
        self.timings = timings
        self.total_time = sum(t.total_time for t in timings.values())
        self.total_time *= _LineProfiler.get_unit()

    def write_text(self, stream):
        if not path.exists(self.filename):
            stream.write("ERROR: %s\n" % self.filename)
            return
        stream.write("File: %s\n" % self.filename)
        stream.write("Name: %s\n" % self.name)
        stream.write("Total time: %g [sec]\n" % self.total_time)

        linecache.clearcache()
        lines = linecache.getlines(self.filename)
        if self.name != "<module>":
            lines = inspect.getblock(lines[self.firstlineno - 1:])

        template = '%6s %9s %12s  %-s'
        header = template % ("Line", "Hits", "Time", "Code")
        stream.write(header)
        stream.write("\n")
        stream.write("=" * len(header))
        stream.write("\n")

        d = {}
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
        # type: (Union[TextIO, TextIOWrapper]) -> None
        stream.write("Time unit: %s [sec]\n\n" % _LineProfiler.get_unit())
        for stat in self.stats:
            stat.write_text(stream)

    def filter(self, f):
        # type: (FilterType) -> LineProfilerStats
        if isinstance(f, BaseFilter):
            return LineProfilerStats(f.filter(self.stats))
        else:
            return LineProfilerStats(f(self.stats))
