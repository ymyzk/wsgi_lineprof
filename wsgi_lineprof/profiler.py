from _wsgi_lineprof import LineProfiler as _LineProfiler  # Cython

from wsgi_lineprof.stats import LineProfilerStat, LineProfilerStats


class LineProfiler(_LineProfiler):
    def get_stats(self):
        # type: () -> LineProfilerStats
        return LineProfilerStats(
            [LineProfilerStat(code.co_filename,
                              code.co_name,
                              code.co_firstlineno,
                              timings)
             for code, timings in self.results.items()])
