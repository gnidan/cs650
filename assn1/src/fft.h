#ifndef _FFT_H_
#define _FFT_H_

#include <stdlib.h>

#define PI 3.141592653589793238462643383279

typedef void(*fft_func)(double in[], double out[], size_t n);

void fft_four1(double in[], double out[], size_t n);

void fftr2(double in[], double out[], size_t n);
void complexfftr2(double in[], double out[], size_t n);

void fftr2opt(double in[], double out[], size_t n);
void complexfftr2opt(double in[], double out[], size_t n);


struct fft_func_t {
  fft_func func;
  char *name;
  char *desc;
};

static const size_t num_fft_funcs = 5;
static const struct fft_func_t fft_funcs[] = {
  {fft_four1,       "fft_four1",       "Numerical Recipes in C"},

  {fftr2,           "fftr2",           "Radix 2 Recursive FFT"},
  {complexfftr2,    "complexfftr2",    "Radix 2 Recursive FFT (C99 complex type)"},

  {fftr2opt,        "fftr2opt",        "Optimized Radix 2 Recursive FFT"},
  {complexfftr2opt, "complexfftr2opt", "Optimized Radix 2 Recursive FFT (C99 complex type)"},
};

#endif /* _FFT_H_ */
