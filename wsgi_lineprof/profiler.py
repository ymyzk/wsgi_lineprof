import inspect
import itertools
import linecache
from os import path

from _wsgi_lineprof import LineProfiler as _LineProfiler  # Cython


class LineProfiler(_LineProfiler):
    def get_stats(self):
        return LineProfilerStats(
            [LineProfilerStat(code.co_filename,
                              code.co_name,
                              code.co_firstlineno,
                              timings)
             for code, timings in self.results.items()])


class LineProfilerStat(object):
    def __init__(self, filename, name, firstlineno, timings):
        self.filename = filename
        self.name = name
        self.firstlineno = firstlineno
        self.timings = timings

    def write_text(self, stream):
        if not path.exists(self.filename):
            stream.write("ERROR: %s\n" % self.filename)
            return
        stream.write("File: %s\n" % self.filename)
        stream.write("Name: %s\n" % self.name)

        total_time = sum(t.total_time for t in self.timings.values())
        total_time *= LineProfiler.get_unit()
        stream.write("Total time: %g [sec]\n" % total_time)

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


class LineProfilerStats(object):
    def __init__(self, stats):
        self.stats = stats

    def write_text(self, stream):
        stream.write("Time unit: %s [sec]\n\n" % LineProfiler.get_unit())
        for stat in self.stats:
            stat.write_text(stream)
