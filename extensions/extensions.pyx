# cython: language_level=3
from cpython cimport PyObject, PyTrace_LINE, PyTrace_RETURN
from header cimport (
    Py_tracefunc,
    PyEval_SetTrace,
    PyFrame_GetCode,
    PyFrame_GetLineNumber,
    PyFrameObject,
)

# It's better if we can use libc.stdint.uint64_t
# but it produces #include <stdint.h> in the generated C code
# Old Windows compilers don't support this.
# from libc.stdint cimport uint64_t
ctypedef unsigned long long uint64_t


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
        PyEval_SetTrace(<Py_tracefunc>python_trace_callback, self)

    def _enable_noop(self):
        PyEval_SetTrace(<Py_tracefunc>python_trace_noop_callback, self)

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

    def __add__(self, other):
        if not isinstance(other, LineTiming):
            return NotImplemented
        if self.code != other.code:
            raise ValueError
        if self.lineno != other.lineno:
            raise ValueError
        res = LineTiming(self.code, self.lineno)
        res.total_time = self.total_time + other.total_time
        res.n_hits = self.n_hits + other.n_hits
        return res

    def __copy__(self):
        res = LineTiming(self.code, self.lineno)
        res.total_time = self.total_time
        res.n_hits = self.n_hits
        return res

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
    IF PY_MAJOR_VERSION >= 3 and PY_MINOR_VERSION >= 9:
        code = <object>PyFrame_GetCode(py_frame)
    ELSE:
        code = <object>py_frame.f_code

    if code in last_time:
        results = self.results
        if code in results:
            result_code = results[code]
        else:
            result_code = results[code] = {}

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
        line = PyFrame_GetLineNumber(py_frame)
        last_time[code] = LastTime(line, hpTimer())

    return 0


cdef int python_trace_noop_callback(object self_, PyFrameObject *py_frame, int what,
                                    PyObject *arg):
    return 0
