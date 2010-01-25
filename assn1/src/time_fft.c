#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>

#include "fft.h"
#include "test.h"

#ifdef PAPI
# if defined(__STDC__)
#  if defined(__STDC_VERSION__)
#   if (__STDC_VERSION__ >= 199901L)
typedef char * caddr_t;
#   endif
#  endif
# endif

#define MIN(A,B) ((A) < (B) ? (A) : (B))
#define MAX(A,B) ((A) > (B) ? (A) : (B))

#include <papi.h>
static int PAPI_EVENTS[] = { PAPI_TOT_CYC, PAPI_TOT_INS,
                             PAPI_FP_OPS, PAPI_L1_DCM };
static size_t NUM_EVENTS = 4;
#endif

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

  const test_func test = test_funcs[test_idx].func;
  test(in, n);

  const fft_func fft = fft_funcs[fft_idx].func;
  const init_func init = fft_funcs[fft_idx].init;
  const destroy_func destroy = fft_funcs[fft_idx].destroy;

#ifdef PAPI
  long long *values = (long long *) calloc(sizeof(long long), iters * NUM_EVENTS);
	int ret;
  if ((ret = PAPI_library_init(PAPI_VER_CURRENT)) != PAPI_VER_CURRENT) {
    fprintf(stderr, "PAPI_library_init error %d: %s\n",ret,PAPI_strerror(ret));
    exit(EXIT_FAILURE);
  }

  int EventSet = PAPI_NULL;
  if ((ret = PAPI_create_eventset(&EventSet)) != PAPI_OK) {
    fprintf(stderr, "PAPI_create_eventset error %d: %s\n",ret,PAPI_strerror(ret));
    exit(EXIT_FAILURE);
  }

  if ((ret = PAPI_add_events(EventSet, PAPI_EVENTS, NUM_EVENTS)) != PAPI_OK) {
    fprintf(stderr, "PAPI_add_events error %d: %s\n",ret,PAPI_strerror(ret));
    exit(EXIT_FAILURE);
  }
#endif

  void *fft_data = NULL;
  for (size_t i = 0; i < iters; i++) {
    if (init) {
      fft_data = init(in, n);
    }

#ifdef PAPI
    if ((ret = PAPI_start(EventSet)) != PAPI_OK) {
      fprintf(stderr, "PAPI_start error %d: %s\n",ret,PAPI_strerror(ret));
      exit(EXIT_FAILURE);
    }
#endif

    fft(in, out, n, fft_data);

#ifdef PAPI
    if ((ret = PAPI_stop(EventSet, &values[i * NUM_EVENTS])) != PAPI_OK) {
      fprintf(stderr, "PAPI_start error %d: %s\n",ret,PAPI_strerror(ret));
      exit(EXIT_FAILURE);
    }
#endif

    if (destroy) {
      destroy(fft_data, n);
    }
  }

  const check_func check = test_funcs[test_idx].check;

  if (check) {
    if(!check(out, n)) {
      fprintf(stderr, "Test: Failed!\n");
      for (size_t i = 0; i < n; i++) {
        fprintf(stderr, "%lf\t%lf\n", out[2*i], out[2*i+1]);
      }
    } else {
      //fprintf(stderr, "Test: Passed!\n");
    }
  } else {
    //fprintf(stderr, "Test: No check defined\n");
    //for (size_t i = 0; i < n; i++) {
    //  fprintf(stderr, "%lf\t%lf\n", out[2*i], out[2*i+1]);
    //}
  }

  printf("%s\t%zu", fft_funcs[fft_idx].name, k);

#ifdef PAPI
  for (size_t i = 0; i < NUM_EVENTS; ++i) {
    double ave = 0;
    long long min = LLONG_MAX;
    long long max = LLONG_MIN;

    for (size_t j = 0; j < iters; ++j) {
      ave += values[j*NUM_EVENTS+i];
      min = MIN(min, values[j*NUM_EVENTS+i]);
      max = MAX(max, values[j*NUM_EVENTS+i]);
    }
    ave /= iters;

    printf("\t%lf\t%lld\t%lld", ave, min, max);
  }
  free(values);
#endif

  printf("\n");

  free(in);
  free(out);
  return 0;
}
