#include <stdlib.h>
#include <stdio.h>

#include "time.h"

#ifdef PAPI
#include <papi.h>

void papi_init(const int events[], size_t n) {
  if (PAPI_VER_CURRENT != PAPI_library_init(PAPI_VER_CURRENT)) {
    fprintf(stderr, "PAPI_library_init error\n");
    exit(EXIT_FAILURE);
  }

  const size_t max = PAPI_num_counters();
  if (n > max) {
    fprintf(stderr, "This machine only supports %zu\n", max);
  }

  for (size_t i = 0; i < n; ++i) {
    if (PAPI_OK != PAPI_query_event(event_code)) {
      fprintf(stderr, "Cannot count event 0x%x\n", events[i]);
      exit(EXIT_FAILURE);
    }
  }
}

#endif
