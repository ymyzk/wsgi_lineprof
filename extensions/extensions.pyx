# cython: language_level=2
from cpython cimport PyObject
from libc.stdint cimport uint64_t

from header cimport (
    PyEval_SetTrace, PyFrameObject, PyTrace_LINE, PyTrace_RETURN
)


cdef extern from "timer.h":
    uint64_t hpTimer()
    double hpTimerUnit()
    char[] HP_TIMER_IMPLEMENTATION


cdef class LineProfiler:
    cdef public dict results
    cdef public dict last_time

    def __init__(self):
        self.results = {}
        self.last_time = {}

    def enable(self):
        PyEval_SetTrace(python_trace_callback, self)

    def disable(self):
        PyEval_SetTrace(NULL, <object>NULL)

    def reset(self):
        self.results = {}
        self.last_time = {}

    @staticmethod
    def get_timer():
        return hpTimer()

    @staticmethod
    def get_timer_implementation():
        if isinstance(HP_TIMER_IMPLEMENTATION, str):
            return HP_TIMER_IMPLEMENTATION
        return HP_TIMER_IMPLEMENTATION.decode("ascii")

    @staticmethod
    def get_unit():
        return hpTimerUnit()


cdef class LineTiming:
    cdef public object code
    cdef public int lineno
    cdef public uint64_t total_time
    cdef public long n_hits

    def __init__(self, object code, int lineno):
        self.code = code
        self.lineno = lineno
        self.total_time = 0
        self.n_hits = 0

    cdef hit(self, uint64_t dt):
            self.n_hits += 1
            self.total_time += dt

    def as_tuple(self):
        return self.lineno, self.n_hits, self.total_time

    def __repr__(self):
        return '<LineTiming for %r lineno: %r n_hits: %r total_time: %r>' % (
            self.code, self.lineno, self.n_hits, <long>self.total_time)


cdef class LastTime:
    cdef int f_lineno
    cdef uint64_t time

    def __cinit__(self, int f_lineno, uint64_t time):
        self.f_lineno = f_lineno
        self.time = time


cdef int python_trace_callback(object self_, PyFrameObject *py_frame, int what,
                               PyObject *arg):
    cdef LineProfiler self
    cdef dict results
    cdef dict result_code
    cdef dict last_time
    cdef LineTiming entry
    cdef LastTime old
    cdef object code
    cdef uint64_t time
    cdef int lineno

    if what != PyTrace_LINE and what != PyTrace_RETURN:
        return 0

    time = hpTimer()

    self = <LineProfiler>self_
    last_time = self.last_time
    results = self.results
    code = <object>py_frame.f_code

    if code not in results:
        results[code] = {}

    if code in last_time:
        result_code = results[code]
        old = last_time[code]
        lineno = old.f_lineno

        if lineno not in result_code:
            result_code[lineno] = entry = LineTiming(code, lineno)
        else:
            entry = result_code[lineno]

        entry.hit(time - old.time)

        if what == PyTrace_RETURN:
            del last_time[code]

    if what == PyTrace_LINE:
        last_time[code] = LastTime(py_frame.f_lineno, hpTimer())

    return 0
