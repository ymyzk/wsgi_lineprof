import inspect
import itertools
import linecache
from abc import ABCMeta, abstractmethod
from os import path
from typing import Any, Dict, Sequence

import colorama

from wsgi_lineprof.stats import LineProfilerStat, LineProfilerStats
from wsgi_lineprof.types import Stream


class BaseFormatter(metaclass=ABCMeta):
    def __init__(self, *kwargs: Any) -> None:
        return

    @abstractmethod
    def format_stats(self, stats: LineProfilerStats, stream: Stream) -> None:
        return


class TextFormatter(BaseFormatter):
    def __init__(self, color: bool = False) -> None:
        self.color = color

    def format_stats(self, stats: LineProfilerStats, stream: Stream) -> None:
        unit = stats.unit
        stream.write("Time unit: %s [sec]\n\n" % unit)
        for stat in stats.stats:
            self.format_stat(stat, stream, unit)

    def format_stat(self, stat: LineProfilerStat, stream: Stream, unit: float) -> None:
        stream.write("File: %s\n" % stat.filename)
        stream.write("Name: %s\n" % stat.name)
        total_time = stat.total_time * unit
        stream.write("Total time: %g [sec]\n" % total_time)
        if not path.exists(stat.filename):
            # e.g., filename is <frozen importlib._bootstrap>
            stream.write("WARNING: Cannot find a file\n")
            return

        linecache.clearcache()
        lines: Sequence[str] = linecache.getlines(stat.filename)
        if stat.name != "<module>":
            lines = inspect.getblock(lines[stat.firstlineno - 1 :])

        template = "%6s %9s %12s %8s %7s  %-s"
        header = template % ("Line", "Hits", "Time", "Per Hit", "% Time", "Code")
        stream.write(header)
        stream.write("\n")
        stream.write("=" * len(header))
        stream.write("\n")

        d: Dict[int, Dict[str, Any]] = {}
        for i, code in zip(itertools.count(stat.firstlineno), lines):
            timing = stat.timings.get(i)
            if timing is None:
                d[i] = {
                    "hits": "",
                    "time": "",
                    "per_hit": "",
                    "percent": "",
                    "code": code,
                    "style": self.style_for_percent(0),
                }
            else:
                if stat.total_time == 0:
                    # TODO: Consider a better way to handle when total_time is 0
                    percent = 0.0
                else:
                    percent = 100 * timing.total_time / stat.total_time
                d[i] = {
                    "hits": timing.n_hits,
                    "time": timing.total_time,
                    "per_hit": "%.1f" % (timing.total_time / timing.n_hits),
                    "percent": "%.1f" % percent,
                    "code": code,
                    "style": self.style_for_percent(percent),
                }
        if self.color:
            colorama.init()
        for i in sorted(d.keys()):
            r = d[i]
            if self.color:
                stream.write(r["style"])
            stream.write(
                template
                % (i, r["hits"], r["time"], r["per_hit"], r["percent"], r["code"])
            )
        if self.color:
            stream.write(colorama.Style.RESET_ALL)
            colorama.deinit()
        stream.write("\n")

    # TODO: Make constants (percent/color) configurable
    def style_for_percent(self, percent: float) -> str:
        """Returns ANSI style for a given percent"""
        if percent < 0.2:
            return colorama.Fore.LIGHTBLACK_EX
        elif percent >= 50:
            return colorama.Fore.RED
        elif percent >= 5:
            return colorama.Fore.YELLOW
        else:
            return colorama.Fore.WHITE
