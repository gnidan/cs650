#ifndef _FFT_H_
#define _FFT_H_

#include <stdlib.h>

#define PI 3.141592653589793238462643383279

typedef void(*fft_func)(double in[], double out[], size_t n, void *data);
typedef void *(*init_func)(double in[], size_t n);
typedef void(*destroy_func)(void *data, size_t n);

void fft_four1(double in[], double out[], size_t n, void *data);
void *four1_init(double in[], size_t n);
void four1_destroy(void *data, size_t n);

void fftr2(double in[], double out[], size_t n, void *data);
void fftr2opt(double in[], double out[], size_t n, void *data);

void complexfftr2(double in[], double out[], size_t n, void *data);
void complexfftr2opt(double in[], double out[], size_t n, void *data);

void kd_fftr2(double in[], double out[], size_t n, void *data);
void kd_fftr2_opt(double in[], double out[], size_t n, void *data);

#ifdef FFTW
void fftw(double in[], double out[], size_t n, void *data);
void *fftw_init(double in[], size_t n);
void fftw_destroy(void *data, size_t n);
#endif

struct fft_func_t {
  fft_func func;
  init_func init;
  destroy_func destroy;
  char *name;
  char *desc;
};

#ifdef FFTW
static const size_t num_fft_funcs = 6;
#else
static const size_t num_fft_funcs = 7;
#endif
static const struct fft_func_t fft_funcs[] = {
  {fftr2,           NULL,       NULL,          "fftr2",           "Radix 2 Recursive FFT"},
  {fftr2opt,        NULL,       NULL,          "fftr2opt",        "Optimized Radix 2 Recursive FFT"},

  {complexfftr2,    NULL,       NULL,          "complexfftr2",    "Radix 2 Recursive FFT (C99 complex type)"},
  {complexfftr2opt, NULL,       NULL,          "complexfftr2opt", "Optimized Radix 2 Recursive FFT (C99 complex type)"},

  {kd_fftr2,        NULL,       NULL,          "kd_fftr2",        "Keith's Radix 2 Recursive FFT"},
  {kd_fftr2_opt,    NULL,       NULL,          "kd_fftr2_opt",    "Keith's Optimized Radix 2 Recursive FFT"},

  {fft_four1,       four1_init, four1_destroy, "fft_four1",       "Numerical Recipes in C"},

#ifdef FFTW
  {fftw,            fftw_init,  fftw_destroy,  "fftw",            "FFTW 2.1.5"},
#endif 
};

#endif /* _FFT_H_ */
