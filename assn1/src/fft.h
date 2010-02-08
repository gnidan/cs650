#ifndef _FFT_H_
#define _FFT_H_

#include <stdlib.h>

#define PI 3.141592653589793238462643383279

typedef void(*fft_func)(double in[], double out[], size_t n, void *data);
typedef void *(*init_func)(double in[], size_t n);
typedef void(*destroy_func)(void *data, size_t n);

void fftr2(double in[], double out[], size_t n, void *data);
void fftr2opt(double in[], double out[], size_t n, void *data);

void complexfftr2(double in[], double out[], size_t n, void *data);
void complexfftr2opt(double in[], double out[], size_t n, void *data);

void kd_fftr2(double in[], double out[], size_t n, void *data);
void kd_fftr2_opt(double in[], double out[], size_t n, void *data);

void fft_rec4(double in[], double out[], size_t n, void *data);
void fft_buf_rec4(double in[], double out[], size_t n, void *data);
void *fft_rec4_init(double in[], size_t n);
void fft_rec4_destroy(void *data, size_t n);

<<<<<<< HEAD
void gnd_fftr2(double in[], double out[], size_t n);

#ifdef FFTW
void fftw(double in[], double out[], size_t n);
=======
void fft_four1(double in[], double out[], size_t n, void *data);
void *four1_init(double in[], size_t n);
void four1_destroy(void *data, size_t n);

#ifdef FFTW
void fft_fftw(double in[], double out[], size_t n, void *data);
void *fftw_estimate_init(double in[], size_t n);
void *fftw_measure_init(double in[], size_t n);
void fftw_destroy(void *data, size_t n);
>>>>>>> c5eddd98fbc801fe9c169601d90298712dcf2831
#endif

struct fft_func_t {
  fft_func func;
  init_func init;
  destroy_func destroy;
  char *name;
  char *desc;
};

#ifdef FFTW
<<<<<<< HEAD
static const size_t num_fft_funcs = 9;
#else
static const size_t num_fft_funcs = 8;
#endif

static const struct fft_func_t fft_funcs[] = {
  {fft_four1,       "fft_four1",       "Numerical Recipes in C"},

#ifdef FFTW
  {fftw,            "fftw",            "FFTW 2.1.5"},
#endif
=======
static const size_t num_fft_funcs = 11;
#else
static const size_t num_fft_funcs = 9;
#endif
static const struct fft_func_t fft_funcs[] = {
  {fftr2,           NULL,               NULL,             "fftr2",           "Radix 2 Recursive FFT"},
  {fftr2opt,        NULL,               NULL,             "fftr2opt",        "Optimized Radix 2 Recursive FFT"},

  {complexfftr2,    NULL,               NULL,             "complexfftr2",    "Radix 2 Recursive FFT (C99 complex type)"},
  {complexfftr2opt, NULL,               NULL,             "complexfftr2opt", "Optimized Radix 2 Recursive FFT (C99 complex type)"},
>>>>>>> c5eddd98fbc801fe9c169601d90298712dcf2831

  {kd_fftr2,        NULL,               NULL,             "kd_fftr2",        "Keith's Radix 2 Recursive FFT"},
  {kd_fftr2_opt,    NULL,               NULL,             "kd_fftr2_opt",    "Keith's Optimized Radix 2 Recursive FFT"},

  {fft_four1,       four1_init,         four1_destroy,    "fft_four1",       "Numerical Recipes in C"},

  {fft_rec4,        fft_rec4_init,      fft_rec4_destroy, "DFT_rec",         "Fast Numerical Code Radix 4 Recursive FFT"},
  {fft_buf_rec4,    fft_rec4_init,      fft_rec4_destroy, "DFT_buf_rec",     "Fast Numerical Code Radix 4 Buffered Recursive FFT (Threshold = 16)"},

<<<<<<< HEAD
  {gnd_fftr2,       "gnd_fftr2",       "Nick's Radix 2 Recursive FFT"}

=======
#ifdef FFTW
  {fft_fftw,        fftw_estimate_init, fftw_destroy,     "fftw_estimate",   "FFTW 2.1.5 Estiamte"},
  {fft_fftw,        fftw_estimate_init, fftw_destroy,     "fftw_measure",    "FFTW 2.1.5 Measure"},
#endif
>>>>>>> c5eddd98fbc801fe9c169601d90298712dcf2831
};

#endif /* _FFT_H_ */
