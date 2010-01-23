#include <math.h>
#include <complex.h>
#include "fft.h"

void four1(double data[], unsigned long nn, int isign);
static const int isign = -1;

void fft_four1(double data[], size_t n) {
  four1(data-1, n, isign);
}

//Recursive Radix-2 FFT
void fftr2(double data[], size_t n) {
  if (n == 1)
    return;

  const size_t np = n/2;

  double *E = (double *) malloc(sizeof(double) * np * 2);
  double *O = (double *) malloc(sizeof(double) * np * 2);

  for (size_t i = 0; i < np; i++) {
    E[2*i  ] = data[4*i  ];
    E[2*i+1] = data[4*i+1];
    O[2*i  ] = data[4*i+2];
    O[2*i+1] = data[4*i+3];
  }

  fftr2(E, np);
  fftr2(O, np);

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
    double Xr = O[2*k  ] * T[2*k  ] - O[2*k+1] * T[2*k+1];
    double Xi = O[2*k+1] * T[2*k  ] + O[2*k  ] * T[2*k+1];

    data[2*k       ] = E[2*k  ] + Xr;
    data[2*k     +1] = E[2*k+1] + Xi;
    data[2*k+2*np  ] = E[2*k  ] - Xr;
    data[2*k+2*np+1] = E[2*k+1] - Xi;
  }

  free(T);
  free(E);
  free(O);
}

//fftr2 implemented using C99 complex type. The same as a double array but cleaner
static void _complexfftr2(double complex data[], size_t n) {
  if (n == 1)
    return;

  const size_t np = n/2;

  double complex *E = (double complex *) malloc(sizeof(double complex) * np);
  double complex *O = (double complex *) malloc(sizeof(double complex) * np);

  for (size_t i = 0; i < np; i++) {
    E[i] = data[2*i  ];
    O[i] = data[2*i+1];
  }

  _complexfftr2(E, np);
  _complexfftr2(O, np);

  double complex *T = (double complex *) malloc(sizeof(double complex) * np);
  for (size_t k = 0; k < np; k++) {
    double theta = 2 * PI * k / n;
    T[k] = cos(theta) - sin(theta)*I;
  }

  for (size_t k = 0; k < np; k++) {
    double complex X = O[k] * T[k];

    data[k   ] = E[k] + X;
    data[k+np] = E[k] - X;
  }

  free(T);
  free(E);
  free(O);
}

void complexfftr2(double data[], size_t n) {
  _complexfftr2((double complex *) data, n);
}

static void _fftr2opt(double data[], size_t n, size_t sx, size_t sy, double wnr, double wni) {
  if (n == 1)
    return;

  const size_t np = n/2;

  double *E = (double *) malloc(sizeof(double) * np * 2);
  double *O = (double *) malloc(sizeof(double) * np * 2);

  for (size_t i = 0; i < np; i++) {
    E[2*i  ] = data[4*i  ];
    E[2*i+1] = data[4*i+1];
    O[2*i  ] = data[4*i+2];
    O[2*i+1] = data[4*i+3];
  }

  //wn2 = wn * wn
  double wn2r = wnr * wnr - wni * wni;
  double wn2i = 2 * wnr * wni;
  _fftr2opt(E, np, sx, sy, wn2r, wn2i);
  _fftr2opt(O, np, sx, sy, wn2r, wn2i);

  double wr = 1.0;
  double wi = 0.0;

  for (size_t k = 0; k < np; k++) {
    double Xr = O[2*k  ] * wr - O[2*k+1] * wi;
    double Xi = O[2*k+1] * wr + O[2*k  ] * wi;

    data[2*k       ] = E[2*k  ] + Xr;
    data[2*k     +1] = E[2*k+1] + Xi;
    data[2*k+2*np  ] = E[2*k  ] - Xr;
    data[2*k+2*np+1] = E[2*k+1] - Xi;

    //w = w * wn
    double wr_old = wr;
    wr = wr * wnr - wi * wni;
    wi = wi * wnr + wr_old * wni;
  }

  free(E);
  free(O);
}

void fftr2opt(double data[], size_t n) {
  const double theta = 2 * PI / n;
  _fftr2opt(data, n, 1, 1, cos(theta), -sin(theta));
}

//fftr2 implemented using C99 complex type. The same as a double array but cleaner
static void _complexfftr2opt(double complex data[], size_t n, size_t sx, size_t sy,
                             const double complex wn) {

  if (n == 1)
    return;

  const size_t np = n/2;

  double complex *E = (double complex *) malloc(sizeof(double complex) * np);
  double complex *O = (double complex *) malloc(sizeof(double complex) * np);

  for (size_t i = 0; i < np; i++) {
    E[i] = data[2*i  ];
    O[i] = data[2*i+1];
  }

  const double complex wn2 = wn * wn;
  _complexfftr2opt(E, np, sx, sy, wn2);
  _complexfftr2opt(O, np, sx, sy, wn2);

  double complex w = 1;

  for (size_t k = 0; k < np; k++) {
    double complex X = O[k] * w;
    data[k   ] = E[k] + X;
    data[k+np] = E[k] - X;
    w = w * wn;
  }

  free(E);
  free(O);
}

void complexfftr2opt(double data[], size_t n) {
  const double theta = 2 * PI / n;
  _complexfftr2opt((double complex *) data, n, 1, 1, cos(theta) - sin(theta)*I);
}
