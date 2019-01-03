import sys

from wsgi_lineprof.profiler import LineProfiler, LineProfilerStats


class TestLineProfiler(object):
    def test_get_timer(self):
        timer = LineProfiler.get_timer()
        if sys.version_info >= (3,):
            assert isinstance(timer, int)
        else:
            assert isinstance(timer, int) or isinstance(timer, long)

    def test_get_timer_is_monotonic(self):
        timer1 = LineProfiler.get_timer()
        timer2 = LineProfiler.get_timer()
        assert timer1 <= timer2

    def test_get_timer_implementation(self):
        implementation = LineProfiler.get_timer_implementation()
        assert isinstance(implementation, str)
        assert len(implementation) > 0

    def test_get_unit(self):
        unit = LineProfiler.get_unit()
        assert isinstance(unit, float)
        assert unit > 0

    def test_get_stats(self):
        def func(x, y):
            return x + y

        subject = LineProfiler()
        subject.results = {
            func.__code__: {}
        }

        stats = subject.get_stats()
        assert isinstance(stats, LineProfilerStats)
