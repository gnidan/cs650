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
    fprintf(stderr, "\t%zu\t%s\t%s\n", i, fft_funcs[i].name, fft_funcs[i].desc);
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

  const fft_func fft = fft_funcs[fft_idx].func;
  const test_func test = test_funcs[test_idx].func;
  const check_func check = test_funcs[test_idx].check;

  const size_t n = 1 << k;
  double *data = (double *) malloc(sizeof(double) * 2*n);

  printf("fft_func = %s\tk = %zu\tn = %zu\n", fft_funcs[fft_idx].name, k, n);

  for (size_t iter = 0; iter < iters; iter++) {
    test(data, n);
    fft(data, n);
  }

  if (check) {
    if(check(data, n)) {
      printf("Test: Passed!\n");
    } else {
      printf("Test: Failed!\n");
      for (size_t i = 0; i < n; i++) {
        printf("%lf\t%lf\n", data[2*i], data[2*i+1]);
      }
    }
  } else {
    printf("Test: No check defined\n");
    for (size_t i = 0; i < n; i++) {
      printf("%lf\t%lf\n", data[2*i], data[2*i+1]);
    }
  }

  free(data);

  return 0;
}
