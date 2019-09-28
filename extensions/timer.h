#include "Python.h"

#ifdef _MSC_VER
typedef unsigned __int64 uint64_t;
#else
#include <stdint.h>
#endif

uint64_t hpTimer(void);
double hpTimerUnit(void);
extern const char HP_TIMER_IMPLEMENTATION[];
