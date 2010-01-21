#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "fft.h"

#define PI 3.141592653589793238462643383279

static const int isign = 1;

int main(int argc, char *argv[]) {

  if (argc < 3) {
    fprintf(stderr, "%s k iters\n", argv[0]);
    return -1;
  }

  const size_t k = (size_t) strtoul(argv[1], NULL, 10);
  const size_t iters = (size_t) strtoul(argv[2], NULL, 10);

  const size_t n = 1 << k;
  double *data = (double *) malloc(sizeof(double) * 2*n);

  for (size_t iter = 0; iter < iters; iter++) {
    for (size_t i = 0; i < n; i++) {
      data[2*i]   =  cos(10*(double)i/(double)n*2.0*PI);
      data[2*i+1] = -sin(10*(double)i/(double)n*2.0*PI);
    }
    four1(data-1, n, isign);
  }

  printf("k = %zu, n = %zu\n", k, n);
  for (size_t i = 0; i < n; i++) {
    printf("%lf\t%lf\n", data[2*i], data[2*i+1]);
  }

  free(data);

  return 0;
}
