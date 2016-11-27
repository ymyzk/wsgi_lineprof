from cpython cimport PyObject

from header cimport (
    PyEval_SetTrace, PyFrameObject, Py_tracefunc, PyEval_SetTrace,
    PY_LONG_LONG, PyTrace_LINE, PyTrace_RETURN
)


cdef extern from "timer.h":
    PY_LONG_LONG hpTimer()
    double hpTimerUnit()


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

    @staticmethod
    def get_unit():
        return hpTimerUnit()


cdef class LineTiming:
    cdef public object code
    cdef public int lineno
    cdef public PY_LONG_LONG total_time
    cdef public long n_hits

    def __init__(self, object code, int lineno):
        self.code = code
        self.lineno = lineno
        self.total_time = 0
        self.n_hits = 0

    cdef hit(self, PY_LONG_LONG dt):
            self.n_hits += 1
            self.total_time += dt

    def as_tuple(self):
        return self.lineno, self.n_hits, self.total_time

    def __repr__(self):
        return '<LineTiming for %r lineno: %r n_hits: %r total_time: %r>' % (
            self.code, self.lineno, self.n_hits, <long>self.total_time)


cdef class LastTime:
    cdef int f_lineno
    cdef PY_LONG_LONG time

    def __cinit__(self, int f_lineno, PY_LONG_LONG time):
        self.f_lineno = f_lineno
        self.time = time


cdef int python_trace_callback(object self_, PyFrameObject *py_frame, int what,
                               PyObject *arg):
    cdef LineProfiler self
    cdef dict results
    cdef dict last_time
    cdef LineTiming entry
    cdef LastTime old
    cdef object code
    cdef PY_LONG_LONG time
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
        old = last_time[code]
        lineno = old.f_lineno

        if lineno not in results[code]:
            results[code][lineno] = entry = LineTiming(code, lineno)
        else:
            entry = results[code][lineno]

        entry.hit(time - old.time)

        if what == PyTrace_RETURN:
            del last_time[code]

    if what == PyTrace_LINE:
        last_time[code] = LastTime(py_frame.f_lineno, hpTimer())

    return 0
