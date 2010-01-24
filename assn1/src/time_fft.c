#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "fft.h"
#include "test.h"

#define PI 3.141592653589793238462643383279

static void usage() {
  fprintf(stderr, "usage: time_fft k iters fft_func test_func\n");

  fprintf(stderr, "\nfft_func values (use integer index):\n");
  for (size_t i = 0; i < num_fft_funcs; i++) {
    fprintf(stderr, "\t%zu\t%-20s\t%s\n", i, fft_funcs[i].name, fft_funcs[i].desc);
  }

  fprintf(stderr, "\ntest_func values (use integer index):\n");
  for (size_t i = 0; i < num_test_funcs; i++) {
    fprintf(stderr, "\t%zu\t%s\t%s\n", i, test_funcs[i].name, test_funcs[i].desc);
  }

  exit(EXIT_FAILURE);
}

int main(int argc, char *argv[]) {

  if (argc < 5)
    usage();

  const size_t k = (size_t) strtoul(argv[1], NULL, 10);
  const size_t iters = (size_t) strtoul(argv[2], NULL, 10);
  const size_t fft_idx = (size_t) strtoul(argv[3], NULL, 10);
  const size_t test_idx = (size_t) strtoul(argv[4], NULL, 10);

  if (fft_idx >= num_fft_funcs || test_idx >= num_test_funcs)
    usage();

  const size_t n = 1 << k;
  double *in = (double *) malloc(sizeof(double) * 2*n);
  double *out = (double *) malloc(sizeof(double) * 2*n);

  printf("%-20s\t%zu\n", fft_funcs[fft_idx].name, n);

  const test_func test = test_funcs[test_idx].func;
  test(in, n);

  const fft_func fft = fft_funcs[fft_idx].func;
  const init_func init = fft_funcs[fft_idx].init;
  const destroy_func destroy = fft_funcs[fft_idx].init;

#ifdef PAPI
  long long *values = (long long *) calloc(sizeof(long long),
                                           iters * DEFAULT_EVENT_COUNT);

  papi_init(DEFAULT_EVENTS, DEFAULT_EVENT_COUNT);

  if (PAPI_start_counters(DEFAULT_EVENTS, DEFAULT_EVENT_COUNT) != PAPI_OK) {
    fprintf(stderr, "Cannot start PAPI counters\n");
    exit(EXIT_FAILURE);
  }
#endif

  void *fft_data = NULL;
  for (size_t iter = 0; iter < iters; iter++) {
    if (init) {
      fft_data = init(in, n);
    }

#ifdef PAPI
    if (PAPI_read_counters(values, DEFAULT_EVENT_COUNT) != PAPI_OK) {
      fprintf(stderr, "Cannot read PAPI counters\n");
      exit(EXIT_FAILURE);
    }
#endif

    fft(in, out, n, fft_data);

#ifdef PAPI
    if (PAPI_read_counters(values, DEFAULT_EVENT_COUNT) != PAPI_OK) {
      fprintf(stderr, "Cannot read PAPI counters\n");
      exit(EXIT_FAILURE);
    }
#endif

    if (destroy) {
      destroy(fft_data, n);
    }
  }

#ifdef PAPI
  if (PAPI_stop_counters(values, DEFAULT_EVENT_COUNT) != PAPI_OK) {
    fprintf(stderr, "Cannot stop PAPI counters\n");
    exit(EXIT_FAILURE);
  }
#endif

  const check_func check = test_funcs[test_idx].check;

  if (check) {
    if(!check(out, n)) {
      fprintf(stderr, "Test: Failed!\n");
      for (size_t i = 0; i < n; i++) {
        fprintf(stderr, "%lf\t%lf\n", out[2*i], out[2*i+1]);
      }
    } else {
      fprintf(stderr, "Test: Passed!\n");
    }
  } else {
    fprintf(stderr, "Test: No check defined\n");
    for (size_t i = 0; i < n; i++) {
      fprintf(stderr, "%lf\t%lf\n", out[2*i], out[2*i+1]);
    }
  }

  free(in);
  free(out);
  return 0;
}
