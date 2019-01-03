from cpython cimport PyObject


cdef extern from "Python.h":
    ctypedef struct PyCodeObject:
        int       co_argcount
        int       co_nlocals
        int       co_stacksize
        int       co_flags
        PyObject *co_code
        PyObject *co_consts
        PyObject *co_names
        PyObject *co_varnames
        PyObject *co_freevars
        PyObject *co_cellvars
        PyObject *co_filename
        PyObject *co_name
        int       co_firstlineno
        PyObject *co_lnotab

    ctypedef struct PyFrameObject:
        PyFrameObject *f_back
        PyCodeObject  *f_code
        PyObject *f_builtins
        PyObject *f_globals
        PyObject *f_locals
        PyObject *f_trace
        PyObject *f_exc_type
        PyObject *f_exc_value
        PyObject *f_exc_traceback
        int f_lasti
        int f_lineno
        int f_restricted
        int f_iblock
        int f_nlocals
        int f_ncells
        int f_nfreevars
        int f_stacksize

cdef extern from "frameobject.h":
    ctypedef int (*Py_tracefunc)(object self, PyFrameObject *py_frame, int what, PyObject *arg)

cdef extern from "Python.h":
    cdef void PyEval_SetTrace(Py_tracefunc func, object arg)

    cdef int PyTrace_LINE
    cdef int PyTrace_RETURN
