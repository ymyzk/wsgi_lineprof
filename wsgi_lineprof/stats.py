from __future__ import division
import inspect
import itertools
import linecache
from os import path
from typing import Any, Callable, cast, Dict, Iterable, Sequence, Union

import colorama

from wsgi_lineprof.extensions import LineProfiler as _LineProfiler, LineTiming
from wsgi_lineprof.filters import BaseFilter
from wsgi_lineprof.types import Stream


# TODO: Make constants (percent/color) configurable
def style_for_percent(percent):
    # type: (float) -> str
    """Returns ANSI style for a given percent"""
    if percent < 0.2:
        return cast(str, colorama.Fore.LIGHTBLACK_EX)
    elif percent >= 50:
        return cast(str, colorama.Fore.RED)
    elif percent >= 5:
        return cast(str, colorama.Fore.YELLOW)
    else:
        return cast(str, colorama.Fore.WHITE)


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

    def write_text(self, stream, color=False):
        # type: (Stream, bool) -> None
        stream.write("File: %s\n" % self.filename)
        stream.write("Name: %s\n" % self.name)
        total_time = self.total_time * _LineProfiler.get_unit()
        stream.write("Total time: %g [sec]\n" % total_time)
        if not path.exists(self.filename):
            # e.g., filename is <frozen importlib._bootstrap>
            stream.write("WARNING: Cannot fild a file\n")
            return

        linecache.clearcache()
        lines = linecache.getlines(self.filename)  # type: Sequence[str]
        if self.name != "<module>":
            lines = inspect.getblock(lines[self.firstlineno - 1:])

        template = '%6s %9s %12s %8s %7s  %-s'
        header = template % ("Line", "Hits", "Time", "Per Hit", "% Time",
                             "Code")
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
                    "per_hit": "",
                    "percent": "",
                    "code": code,
                    "style": style_for_percent(0),
                }
            else:
                percent = 100 * timing.total_time / self.total_time
                d[i] = {
                    "hits": timing.n_hits,
                    "time": timing.total_time,
                    "per_hit": '%.1f' % (timing.total_time / timing.n_hits),
                    "percent": '%.1f' % percent,
                    "code": code,
                    "style": style_for_percent(percent),
                }
        if color:
            colorama.init()
        for i in sorted(d.keys()):
            r = d[i]
            if color:
                stream.write(r["style"])
            stream.write(template % (i, r["hits"], r["time"], r["per_hit"],
                                     r["percent"], r["code"]))
        if color:
            stream.write(colorama.Style.RESET_ALL)
            colorama.deinit()
        stream.write("\n")


CallableFilterType = Callable[[Iterable[LineProfilerStat]],
                              Iterable[LineProfilerStat]]
FilterType = Union[CallableFilterType, BaseFilter]


class LineProfilerStats(object):
    def __init__(self, stats):
        # type: (Iterable[LineProfilerStat]) -> None
        self.stats = stats

    def write_text(self, stream, color=False):
        # type: (Stream, bool) -> None
        stream.write("Time unit: %s [sec]\n\n" % _LineProfiler.get_unit())
        for stat in self.stats:
            stat.write_text(stream, color=color)

    def filter(self, f):
        # type: (FilterType) -> LineProfilerStats
        if isinstance(f, BaseFilter):
            return LineProfilerStats(f.filter(self.stats))
        else:
            return LineProfilerStats(f(self.stats))
