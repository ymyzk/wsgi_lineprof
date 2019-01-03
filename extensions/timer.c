#include "Python.h"

/*
 * This code is derived from Modules/_lsprof.c in CPython,
 * and modified for this library.
 *
 * The original code is licensed under Python Software Foundation License.
 */

/*** Selection of a high-precision timer ***/

#if defined(MS_WINDOWS)

#include <windows.h>

long long
hpTimer(void)
{
    LARGE_INTEGER li;
    QueryPerformanceCounter(&li);
    return li.QuadPart;
}

double
hpTimerUnit(void)
{
    LARGE_INTEGER li;
    if (QueryPerformanceFrequency(&li))
        return 1.0 / li.QuadPart;
    else
        return 0.000001;  /* unlikely */
}

const char HP_TIMER_IMPLEMENTATION[] = "QueryPerformanceCounter()";

#else

#ifndef HAVE_GETTIMEOFDAY
#error "This module requires gettimeofday() on non-Windows platforms!"
#endif

#include <sys/resource.h>
#include <sys/times.h>

long long
hpTimer(void)
{
    struct timeval tv;
    long long ret;
#ifdef GETTIMEOFDAY_NO_TZ
    gettimeofday(&tv);
#else
    gettimeofday(&tv, (struct timezone *)NULL);
#endif
    ret = tv.tv_sec;
    ret = ret * 1000000 + tv.tv_usec;
    return ret;
}

double
hpTimerUnit(void)
{
    return 0.000001;
}

const char HP_TIMER_IMPLEMENTATION[] = "gettimeofday()";

#endif
