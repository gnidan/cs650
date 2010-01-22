#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "fft.h"

#define PI 3.141592653589793238462643383279

//All reals should equal 1/n, All imaginary values should be 0
static inline void test0(double data[], size_t n) {
  for (size_t i = 0; i < 2*n; i++) {
    data[i] = (i==0);
  }
}

//all sqrt( data[i].r^2 + data[i].i^2) should equal 1/n
static inline void test1(double data[], size_t n) {
  for (size_t i = 0; i < 2*n; i++) {
    data[i] = (i==2);
  }
}

static inline void test2(double data[], size_t n) {
  for (size_t i = 0; i < n; i++) {
    data[2*i  ] = i;
    data[2*i+1] = 0;
  }
}

static inline void test3(double data[], size_t n) {
  for (size_t i = 0; i < 2*n; i++) {
    data[i] = i;
  }
}

static inline void test4(double data[], size_t n) {
  for (size_t i = 0; i < n; i++) {
    data[2*i]   =  cos(10*(double)i/(double)n*2.0*PI);
    data[2*i+1] = -sin(10*(double)i/(double)n*2.0*PI);
  }
}

static const int isign = -1;



int main(int argc, char *argv[]) {

  if (argc < 3) {
    fprintf(stderr, "%s k iters\n", argv[0]);
    return -1;
  }

  const size_t k = (size_t) strtoul(argv[1], NULL, 10);
  const size_t iters = (size_t) strtoul(argv[2], NULL, 10);
  const size_t test = 0;
  const size_t function = 0;

  const size_t n = 1 << k;
  double *data = (double *) malloc(sizeof(double) * 2*n);

  for (size_t iter = 0; iter < iters; iter++) {
    test3(data, n);

    //fft_four1(data, n);
    //fftr2(data, n);
    fftr2opt(data, n);
    //complexfftr2(data, n);
    //complexfftr2opt(data, n);
  }

  printf("k = %zu, n = %zu\n", k, n);
  for (size_t i = 0; i < n; i++) {
    printf("%lf\t%lf\n", data[2*i], data[2*i+1]);
  }

  free(data);

  return 0;
}
