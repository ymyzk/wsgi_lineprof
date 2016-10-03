from wsgi_lineprof.profiler import LineProfiler, LineProfilerStats


class TestLineProfiler(object):
    def test_get_unit(self):
        assert LineProfiler.get_unit() > 0

    def test_get_stats(self):
        def func(x, y):
            return x + y

        subject = LineProfiler()
        subject.results = {
            func.__code__: {}
        }

        stats = subject.get_stats()
        assert isinstance(stats, LineProfilerStats)
