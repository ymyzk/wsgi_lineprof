#include "Python.h"

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

#elif defined(__APPLE__)

#include <mach/mach_time.h>

long long
hpTimer(void)
{
    return mach_absolute_time();
}

double
hpTimerUnit(void)
{
    static mach_timebase_info_data_t timebase;
    static double unit = 0;
    if (timebase.denom == 0) {
        mach_timebase_info(&timebase);
        unit = (double)timebase.numer / (double)timebase.denom * 1e-9;
    }
    return unit;
}

const char HP_TIMER_IMPLEMENTATION[] = "mach_absolute_time()";

#elif defined(HAVE_CLOCK_GETTIME) && defined(CLOCK_MONOTONIC)

long long
hpTimer(void)
{
    struct timespec ts;
    long long ret;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    ret = ts.tv_sec;
    ret = ret * 1000000000 + ts.tv_nsec;
    return ret;
}

double
hpTimerUnit(void)
{
    return 0.000000001;
}

const char HP_TIMER_IMPLEMENTATION[] = "clock_gettime(CLOCK_MONOTONIC)";

#elif defined(HAVE_GETTIMEOFDAY)

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

#else

#error "This module requires clock_gettime(CLOCK_MONOTONIC) or gettimeofday()"

#endif
