from wsgi_lineprof.extensions import LineProfiler as _LineProfiler  # Cython
from wsgi_lineprof.stats import LineProfilerStat, LineProfilerStats


class LineProfiler(_LineProfiler):
    def get_stats(self):
        # type: () -> LineProfilerStats
        return LineProfilerStats(
            [LineProfilerStat(
                # TODO: Improve how to handle empty filename
                code.co_filename if code.co_filename is not None else "",
                code.co_name,
                code.co_firstlineno,
                timings)
             for code, timings in self.results.items()])
