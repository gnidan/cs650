#include <math.h>
#include <complex.h>
#include <string.h>
#include "fft.h"

#include "fft4.h"

#ifdef FFTW
#include <fftw.h>
#endif

void four1(double data[], unsigned long nn, int isign);
static const int isign = -1;


void *four1_init(double in[], size_t n) {
  double *data = malloc(sizeof(double) * 2 * n);
  memcpy(data, in, sizeof(double) * 2 * n);
  return data;
}

void fft_four1(double in[], double out[], size_t n, void *data) {
  four1(((double *)data) - 1, n, isign);
}

void four1_destroy(void *data, size_t n) {
  free(data);
}

/**
 * @brief The "optimized" implementation of the radix 2 fft.  This function
 *        assumes that the size of the input vector is a power of 2.  Error
 *        checking for this fact should be implemented by the calling function.
 *
 * @param in  The array of doubles that represent the input vector.  Each entry
 *            in the input vector uses two entries in the array, the first
 *            entry is the real part and the second entry is the imag part.
 * @param out The array of doublew where the output is placed.
 * @param n   The number of elements in the input vector, thus half the number
 *            of entries in the above array of doubles.
 * @param omega_r The real part of the primitive nth root of unity.
 * @param omega_i The imaginary part of the primitive nth root of unity.
 * @param in_start   The first index in the input array that the current call
 *                   has access to.
 * @param out_start  The first index in the output array that the current call
 *                   has access to.
 * @param stride  The stride parameter so that explicit permutation is
 *                unnecessary.
 */
static void _kd_fftr2_opt (double *in, double *out, unsigned int n,
                           double omega_r, double omega_i, unsigned int in_start,
                           unsigned int out_start, unsigned int stride)
{
  if ( n == 1 )
  {
    out[2 * in_start] = in[2 * out_start];
    out[2 * in_start + 1] = in[2 * out_start + 1];
    return;
  }

  double o_r = omega_r * omega_r - omega_i * omega_i;
  double o_i = 2 * omega_r * omega_i;
  _kd_fftr2_opt (in, out, n / 2, o_r, o_i, in_start, out_start, 2 * stride);
  _kd_fftr2_opt (in, out, n / 2, o_r, o_i, in_start + n/2 ,
                 out_start + stride / 2, 2 * stride);

  unsigned int i;
  o_r = 1.0;
  o_i = 0.0;
  for ( i = 0; i < n; i += 2 )
  {
    /* twiddle */
    double a = o_r * out[2 * in_start + n + i] -
        o_i * out[2 * in_start + n + i + 1];
    double b = o_i * out[2 * in_start + n + i] +
        o_r * out[2 * in_start + n + i + 1];

    /* vector butterfly */
    out[2 * in_start + i] += a;
    out[2 * in_start + i + 1] += b;
    out[2 * in_start + i + n] = out[2 * in_start + i] - 2 * a;
    out[2 * in_start + i + n + 1] = out[2 * in_start + i + 1] - 2 * b;

    /* update power of omega */
    a = o_r; /* reuse a to temporarily store current o_r value */
    o_r = o_r * omega_r - o_i * omega_i;
    o_i = o_i * omega_r + a   * omega_i;
  }
}

void kd_fftr2_opt(double in[], double out[], size_t n, void *data) {
  const double omega_r = cos (2 * PI / (double) n);
  const double omega_i = -sin (2 * PI / (double) n);
  _kd_fftr2_opt(in, out, n, omega_r, omega_i, 0, 0, 2);
}

/**
 * @brief The "naive" implementation of the radix 2 fft.
 *
 * @param in The array of doubles containing the input vector to the fft.
 *           Each complex value uses two entries in the array.  The first
 *           entry contains the real part and the second entry contains the
 *           imaginary part.  That is, if the input is x_0, x_1, ... x_{n-1},
 *           then x_0 = v[0] + i * v[1], x_1 = v[2] + i * v[3], ... ,
 *           x_{n - 1} = v[2 * (n - 1)] + i * v[2 * (n - 1) + 1].
 * @param out The array of doubles where the output of the function is to be
 *            stored.
 * @param n  The size of the input vector, which means that the size of the
 *           input array v is 2 * n.  We assume without checking that this
 *           value is a power of 2.  It is the responsibility of the calling
 *           function to perform this check.
 * @param omega_r  The real part of the primitive nth root of unity.
 * @param omega_i  The imaginary part of the primitvie nth root of unity.
 */
static void _kd_fftr2 (double *in, double *out, unsigned int n,
                       double omega_r, double omega_i)
{
  double *firstHalf, *secondHalf, *permuted, o_r, o_i;
  unsigned int i;

  /* Step 0: Check for base case */
  if ( n == 1 )
  {
    out[0] = in[0];
    out[1] = in[1];
    return;
  }

  permuted   = (double *) malloc (2 * n * sizeof (double));

  /* Step 1: Perform a stride 2 permutation. */
  for ( i = 0; i < n; i += 2 )
  {
    permuted[i]         = in[2 * i];
    permuted[i + 1]     = in[2 * i + 1];
    permuted[i + n]     = in[2 * i + 2];
    permuted[i + n + 1] = in[2 * i + 3];
  }

  firstHalf  = (double *) malloc (n * sizeof (double));
  secondHalf = (double *) malloc (n * sizeof (double));

  /* Step 2: Recursively call this function twice on both halves of the data */
  o_r = omega_r * omega_r - omega_i * omega_i;
  o_i = omega_r * omega_i + omega_r * omega_i;
  _kd_fftr2 (permuted,     firstHalf,  n / 2, o_r, o_i);
  _kd_fftr2 (permuted + n ,secondHalf, n / 2, o_r, o_i);

  free (permuted);

  /* Step 3: "twiddle" the input; multiply the second half of the array by
     successive powers of omega. */
  o_r = 1.0;
  o_i = 0.0;
  for ( i = 0; i < n; i += 2 )
  {
    double a = secondHalf[i];
    double b = secondHalf[i + 1];
    secondHalf[i + 0] = a * o_r - b * o_i;
    secondHalf[i + 1] = a * o_i + b * o_r;
    /* calculate the next power of omega */
    a = o_r;
    b = o_i;
    o_r = a * omega_r - b * omega_i;
    o_i = a * omega_i + b * omega_r;
  }

  /* Step 4: Vector butterfly; the first half of the output is the first
     half of the current vector plus the second half.  The second half of
     the output is the first half minus the second half. */
  for ( i = 0; i < n; i += 2 )
  {
    out[i + 0]     = firstHalf[i] + secondHalf[i];
    out[i + 1]     = firstHalf[i + 1] + secondHalf[i + 1];
    out[i + n + 0] = firstHalf[i] - secondHalf[i];
    out[i + n + 1] = firstHalf[i + 1] - secondHalf[i + 1];
  }

  free (firstHalf);
  free (secondHalf);
  return;
}

void kd_fftr2(double in[], double out[], size_t n, void *data) {
  const double omega_r = cos (2 * PI / (double) n);
  const double omega_i = -sin (2 * PI / (double) n);
  _kd_fftr2(in, out, n, omega_r, omega_i);
}

//Recursive Radix-2 FFT
static void _fftr2(double in[], double out[], size_t n) {
  if (n == 1) {
    out[0] = in[0];
    out[1] = in[1];
    return;
  }

  const size_t np = n/2;

  double *XE = (double *) malloc(sizeof(double) * np * 2);
  double *XO = (double *) malloc(sizeof(double) * np * 2);
  double *YE = (double *) malloc(sizeof(double) * np * 2);
  double *YO = (double *) malloc(sizeof(double) * np * 2);

  for (size_t i = 0; i < n; i+=2) {
    XE[i  ] = in[2*i  ];
    XE[i+1] = in[2*i+1];
    XO[i  ] = in[2*i+2];
    XO[i+1] = in[2*i+3];
  }

  _fftr2(XE, YE, np);
  _fftr2(XO, YO, np);

  //twiddle
  double * T = (double *) malloc(sizeof(double) * np * 2);
  for (size_t k = 0; k < n; k+=2) {
    double theta = PI * k / n;
    T[k  ] = cos(theta);
    T[k+1] = -sin(theta);
  }

  //butterfly
  for (size_t k = 0; k < n; k+=2) {
    //complex multiplication
    double Xr = YO[k  ] * T[k  ] - YO[k+1] * T[k+1];
    double Xi = YO[k+1] * T[k  ] + YO[k  ] * T[k+1];

    out[k       ] = YE[k  ] + Xr;
    out[k     +1] = YE[k+1] + Xi;
    out[k+2*np  ] = YE[k  ] - Xr;
    out[k+2*np+1] = YE[k+1] - Xi;
  }

  free(T);
  free(XE);
  free(XO);
  free(YE);
  free(YO);
}

void fftr2(double in[], double out[], size_t n, void *data) {
  _fftr2(in, out, n);
}

//fftr2 implemented using C99 complex type. The same as a double array but cleaner
static void _complexfftr2(double complex in[], double complex out[], size_t n) {
  if (n == 1) {
    out[0] = in[0];
    return;
  }

  const size_t np = n/2;

  double complex *XE = (double complex *) malloc(sizeof(double complex) * np);
  double complex *XO = (double complex *) malloc(sizeof(double complex) * np);
  double complex *YE = (double complex *) malloc(sizeof(double complex) * np);
  double complex *YO = (double complex *) malloc(sizeof(double complex) * np);

  for (size_t i = 0; i < np; i++) {
    XE[i] = in[2*i  ];
    XO[i] = in[2*i+1];
  }

  _complexfftr2(XE, YE, np);
  _complexfftr2(XO, YO, np);

  double complex *T = (double complex *) malloc(sizeof(double complex) * np);
  for (size_t k = 0; k < np; k++) {
    double theta = 2 * PI * k / n;
    T[k] = cos(theta) - sin(theta)*I;
  }

  for (size_t k = 0; k < np; k++) {
    double complex X = YO[k] * T[k];

    out[k   ] = YE[k] + X;
    out[k+np] = YE[k] - X;
  }

  free(T);
  free(XE);
  free(XO);
  free(YE);
  free(YO);
}

void complexfftr2(double in[], double out[], size_t n, void *data) {
  _complexfftr2((double complex *) in, (double complex *) out, n);
}

static void _fftr2opt(double in[], double out[], size_t n, size_t s, double wnr, double wni) {
  if (n == 1) {
    out[0] = in[s+0];
    out[1] = in[s+1];
    return;
  }

  if (n == 2) {
    out[0] = in[0] + in[s  ];
    out[1] = in[1] + in[s+1];
    out[2] = in[0] - in[s  ];
    out[3] = in[1] - in[s+1];
    return;
  }

  const size_t np = n/2;

  double wn2r = wnr * wnr - wni * wni;
  double wn2i = 2 * wnr * wni;
  _fftr2opt(in,     out,      np, 2*s, wn2r, wn2i);
  _fftr2opt(in+2*s, out+2*np, np, 2*s, wn2r, wn2i);

  double wr = 1.0;
  double wi = 0.0;

  for (size_t k = 0; k < n; k+=2) {
    double Xr = out[k  ] * wr - out[k+1] * wi;
    double Xi = out[k+1] * wr + out[k  ] * wi;

    out[k+2*np  ] = out[k  ] - Xr;
    out[k+2*np+1] = out[k+1] - Xi;
    out[k       ] = out[k  ] + Xr;
    out[2*k   +1] = out[k+1] + Xi;

    //w = w * wn
    double wr_old = wr;
    wr = wr * wnr - wi * wni;
    wi = wi * wnr + wr_old * wni;
  }
}

void fftr2opt(double in[], double out[], size_t n, void *data) {
  const double theta = 2 * PI / n;
  _fftr2opt(in, out, n, 1, cos(theta), -sin(theta));
}

//fftr2 implemented using C99 complex type. The same as a double array but cleaner
static void _complexfftr2opt(double complex in[], double complex out[],
                             size_t n, size_t s, const double complex wn) {

  if (n == 1) {
    out[0] = in[0];
    return;
  }

  const size_t np = n/2;

  const double complex wn2 = wn * wn;
  _complexfftr2opt(in,   out,    np, 2*s, wn2);
  _complexfftr2opt(in+s, out+np, np, 2*s, wn2);

  double complex w = 1;

  for (size_t k = 0; k < np; k++) {
    double complex X = out[k+np] * w;
    out[k+np] = out[k] - X;
    out[k   ] = out[k] + X;
    w = w * wn;
  }
}

void complexfftr2opt(double in[], double out[], size_t n, void *data) {
  const double theta = 2 * PI / n;
  _complexfftr2opt((double complex *) in, (double complex *) out, n, 1, cos(theta) - sin(theta)*I);
}

#ifdef FFTW
void fft_fftw(double in[], double out[], size_t n, void *data) {
  fftw_plan plan = (fftw_plan) data;
  fftw_one(plan, (fftw_complex *) in, (fftw_complex *) out);
}

void *fftw_estimate_init(double in[], size_t n) {
  return (void *) fftw_create_plan(n, FFTW_FORWARD, FFTW_ESTIMATE);
}

void *fftw_measure_init(double in[], size_t n) {
  return (void *) fftw_create_plan(n, FFTW_FORWARD, FFTW_MEASURE);
}

void fftw_destroy(void *data, size_t n) {
  fftw_destroy_plan((fftw_plan) data);
}
#endif

void *fft_rec4_init(double in[], size_t n) {
  init_DFT(n);
  return NULL;
}

void fft_rec4_destroy(void *data, size_t n) {
  destroy_DFT(n);
}

void fft_rec4(double in[], double out[], size_t n, void *data) {
  DFT_rec(n, log4(n), out, in, 1);
}

void fft_buf_rec4(double in[], double out[], size_t n, void *data) {
  DFT_buf_rec(n, log4(n), out, in, 1, 16);
}
