from copy import copy

import pytest

from wsgi_lineprof.extensions import LineTiming


def func():
    return 123


def func2():
    return "hello"


class TestLineTiming:
    def test_as_tuple(self):
        subject = LineTiming(func.__code__, 10)
        assert subject.as_tuple() == (10, 0, 0)

    def test_copy(self):
        timing = LineTiming(func.__code__, 1)
        timing.total_time = 2
        timing.n_hits = 3
        copied = copy(timing)
        copied.total_time = 4
        copied.n_hits = 5
        assert timing.total_time == 2
        assert timing.n_hits == 3

    def test_add_succeeds(self):
        a = LineTiming(func.__code__, 1)
        a.total_time = 2
        a.n_hits = 3
        b = LineTiming(func.__code__, 1)
        b.total_time = 4
        b.n_hits = 5
        c = a + b
        assert a.code == func.__code__
        assert a.lineno == 1
        assert a.total_time == 2
        assert a.n_hits == 3
        assert b.code == func.__code__
        assert b.lineno == 1
        assert b.total_time == 4
        assert b.n_hits == 5
        assert c.code == func.__code__
        assert c.lineno == 1
        assert c.total_time == 6
        assert c.n_hits == 8

    def test_add_not_implemented(self):
        a = LineTiming(func.__code__, 1)
        with pytest.raises(TypeError):
            a + 1

    def test_add_value_error(self):
        a = LineTiming(func.__code__, 1)
        b = LineTiming(func2.__code__, 1)
        c = LineTiming(func.__code__, 2)
        with pytest.raises(ValueError):
            a + b
        with pytest.raises(ValueError):
            a + c
