#include <math.h>
#include <complex.h>
#include <string.h>
#include "fft.h"

void four1(double data[], unsigned long nn, int isign);
static const int isign = -1;

void fft_four1(double in[], double out[], size_t n) {
  memcpy(out, in, sizeof(double) * 2 * n);
  four1(out-1, n, isign);
}

//Recursive Radix-2 FFT
void fftr2(double in[], double out[], size_t n) {
  if (n == 1) {
    out[0] = in[0];
    out[1] = in[1];
    return;
  }

  if (n == 2) {
    out[0] = in[0] + in[2];
    out[1] = in[1] + in[3];
    out[2] = in[0] - in[2];
    out[3] = in[1] - in[3];
    return;
  }

  const size_t np = n/2;

  double *XE = (double *) malloc(sizeof(double) * np * 2);
  double *XO = (double *) malloc(sizeof(double) * np * 2);
  double *YE = (double *) malloc(sizeof(double) * np * 2);
  double *YO = (double *) malloc(sizeof(double) * np * 2);

  for (size_t i = 0; i < np; i++) {
    XE[2*i  ] = in[4*i  ];
    XE[2*i+1] = in[4*i+1];
    XO[2*i  ] = in[4*i+2];
    XO[2*i+1] = in[4*i+3];
  }

  fftr2(XE, YE, np);
  fftr2(XO, YO, np);

  //twiddle
  double * T = (double *) malloc(sizeof(double) * np * 2);
  for (size_t k = 0; k < np; k++) {
    double theta = 2 * PI * k / n;
    T[2*k  ] = cos(theta);
    T[2*k+1] = -sin(theta);
  }

  //butterfly
  for (size_t k = 0; k < np; k++) {
    //complex multiplication
    double Xr = YO[2*k  ] * T[2*k  ] - YO[2*k+1] * T[2*k+1];
    double Xi = YO[2*k+1] * T[2*k  ] + YO[2*k  ] * T[2*k+1];

    out[2*k       ] = YE[2*k  ] + Xr;
    out[2*k     +1] = YE[2*k+1] + Xi;
    out[2*k+2*np  ] = YE[2*k  ] - Xr;
    out[2*k+2*np+1] = YE[2*k+1] - Xi;
  }

  free(T);
  free(XE);
  free(XO);
  free(YE);
  free(YO);
}

//fftr2 implemented using C99 complex type. The same as a double array but cleaner
static void _complexfftr2(double complex in[], double complex out[], size_t n) {
  if (n == 1) {
    out[0] = in[0];
    return;
  }

  if (n == 2) {
    out[0] = in[0] + in[1];
    out[1] = in[0] - in[1];
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

void complexfftr2(double in[], double out[], size_t n) {
  _complexfftr2((double complex *) in, (double complex *) out, n);
}

static void _fftr2opt(double in[], double out[], size_t n, size_t s, double wnr, double wni) {
  if (n == 1) {
    out[0] = in[0];
    out[1] = in[1];
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

  for (size_t k = 0; k < np; k++) {
    double Xr = out[2*k  ] * wr - out[2*k+1] * wi;
    double Xi = out[2*k+1] * wr + out[2*k  ] * wi;

    out[2*k+2*np  ] = out[2*k  ] - Xr;
    out[2*k+2*np+1] = out[2*k+1] - Xi;
    out[2*k       ] = out[2*k  ] + Xr;
    out[2*k     +1] = out[2*k+1] + Xi;

    //w = w * wn
    double wr_old = wr;
    wr = wr * wnr - wi * wni;
    wi = wi * wnr + wr_old * wni;
  }
}

void fftr2opt(double in[], double out[], size_t n) {
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

  if (n == 2) {
    out[0] = in[0] + in[s];
    out[1] = in[0] - in[s];
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

void complexfftr2opt(double in[], double out[], size_t n) {
  const double theta = 2 * PI / n;
  _complexfftr2opt((double complex *) in, (double complex *) out, n, 1, cos(theta) - sin(theta)*I);
}
