#ifndef _FFT_H_
#define _FFT_H_

#include <stdlib.h>

#define PI 3.141592653589793238462643383279

typedef void(*fft_func)(double in[], double out[], size_t n);

void fft_four1(double in[], double out[], size_t n);

void fftr2(double in[], double out[], size_t n);
void fftr2opt(double in[], double out[], size_t n);

void complexfftr2(double in[], double out[], size_t n);
void complexfftr2opt(double in[], double out[], size_t n);

void kd_fftr2(double in[], double out[], size_t n);
void kd_fftr2_opt(double in[], double out[], size_t n);

void fft_fftw(double in[], double out[], size_t n);

struct fft_func_t {
  fft_func func;
  char *name;
  char *desc;
};

static const size_t num_fft_funcs = 7;
static const struct fft_func_t fft_funcs[] = {
  {fftr2,           "fftr2",           "Radix 2 Recursive FFT"},
  {fftr2opt,        "fftr2opt",        "Optimized Radix 2 Recursive FFT"},

  {complexfftr2,    "complexfftr2",    "Radix 2 Recursive FFT (C99 complex type)"},
  {complexfftr2opt, "complexfftr2opt", "Optimized Radix 2 Recursive FFT (C99 complex type)"},

  {kd_fftr2,        "kd_fftr2",        "Keith's Radix 2 Recursive FFT"},
  {kd_fftr2_opt,    "kd_fftr2_opt",    "Keith's Optimized Radix 2 Recursive FFT"},

	{fft_four1,       "fft_four1",       "Numerical Recipes in C"},
#ifdef FFTW
  {fft_fftw,        "fft_fftw",        "FFTW 2.1.5"},
#endif
};

#endif /* _FFT_H_ */
