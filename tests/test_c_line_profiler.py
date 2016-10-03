from _wsgi_lineprof import LineTiming


class TestLineTiming(object):
    def test_as_tuple(self):
        def func():
            return 123

        subject = LineTiming(func.__code__, 10)
        assert subject.as_tuple() == (10, 0, 0)
