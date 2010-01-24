#ifndef _TIME_H_
#define _TIME_H_

#ifdef PAPI
#include <papi.h>

static const int DEFAULT_EVENTS[] = { PAPI_TOT_CYC, PAPI_TOT_INS,
                                      PAPI_FP_OPS, PAPI_L1_DCM };
static const size_t DEFAULT_EVENT_COUNT = 4;

void papi_init(const int events[], size_t n);

#else

#endif

#endif /* _TIME_H_ */
