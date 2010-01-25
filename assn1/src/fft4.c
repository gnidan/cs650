// recursive radix-4 DFT implementation

// compute the exponent
#include <math.h>
#define log4(N) (int)(log(N)/log(4))

// top-level call to DFT function
#define DFT(N, Y, X) DFT_rec(N, log4(N), Y, X, 1)

// DFT kernels
static void DFT4_base(double *Y, double *X, int s);
static void DFT4_twiddle(double *Y, int s, int N, int j);

// recursive radix-4 DFT function
// N: problem size
// Y: output vector
// X: input vector
// s: stride to access X
void DFT_rec(int N, int n, double *Y, double *X, int s) {
  int j;
  if (N==4)
    // Y = DFT_4 X
    DFT4_base(Y, X, s);
  else {
    // Y = (I_4 x DFT_N/4)(LˆN_4) X
    for(j=0; j<4; j++)
      DFT_rec(N/4, n-1, Y+(2*(N/4)*j), X+2*j*s, s*4);
    // Y = (DFT_4 x I_{N/4})(D_N,4) Y
    for(j=0; j<N/4; j++)
      DFT4_twiddle(Y+2*j, N/4, n, j);
  }
}

// cache line size = 2 complex numbers (16 bytes)
# define LS	2

// recursive radix-4 DFT function with buffering
// N: problem size
// Y: output vector
// X: input vector
// s: stride to access X
// th: threshold size to stop buffering
void DFT_buf_rec(int N, int n, double *Y, double *X, int s, int th) {
  int i, j, j1, j2, k;
  // local buffer
  double buf[8*LS];

  if (N==4)
    // Y = DFT_4 X
    DFT4_base(Y, X, s);
  else {
    // Y = (I_4 x DFT_{N/4})(LˆN_4) X

    if (N > th)
      for(j=0; j<4; j++)
        DFT_buf_rec(N/4, n-1, Y+(2*(N/4)*j), X+2*j*s, s*4, th);
    else
      for(j=0; j<4; j++)
        DFT_rec(N/4, n-1, Y+(2*(N/4)*j), X+2*j*s, s*4);

    // Y = (DFT_4 x I_{N/4})(D_{N,4}) Y, buffered for LS
    // j loop tiled by LS
    for(j1=0; j1<N/(4*LS); j1++) {
      // copy 4 chunks of 2*LS double to local buffer
      for(i=0; i<4; i++)
        for(k=0; k<2*LS; k++)
          buf[2*LS*i+k] = Y[(2*LS*j1)+(2*(N/4)*i)+k];

      // perform LS DFT4 on contiguous data
      // buf = (DFT4 Dj x I_LS) buf
      for(j2=0; j2<LS; j2++)
        DFT4_twiddle(buf+2*j2, LS, n, j1*LS+j2);

      // copy 4 chunks of 2*LS double to output
      for(i=0; i<4; i++)
        for(k=0; k<2*LS; k++)
          Y[(2*LS*j1)+(2*(N/4)*i)+k] = buf[2*LS*i+k];
    }
  }
}

// DFT4 implementation
static void DFT4_base(double *Y, double *X, int s) {
  double t0, t1, t2, t3, t4, t5, t6, t7;
  t0 = (X[0] + X[4*s]);
  t1 = (X[2*s] + X[6*s]);
  t2 = (X[1] + X[4*s+1]);
  t3 = (X[2*s+1] + X[6*s+1]);
  t4 = (X[0] - X[4*s]);
  t5 = (X[2*s+1] - X[6*s+1]);
  t6 = (X[1] - X[4*s+1]);
  t7 = (X[2*s] - X[6*s]);
  Y[0] = (t0 + t1);
  Y[1] = (t2 + t3);
  Y[4] = (t0 - t1);
  Y[5] = (t2 - t3);
  Y[2] = (t4 - t5);
  Y[3] = (t6 + t7);
  Y[6] = (t4 + t5);
  Y[7] = (t6 - t7);
}

// C macro for complex multiplication
#define CMPLX_MULT(cr, ci, a, b, idx, s)        \
  { double ar, ai, br, bi;                      \
    ar = a[2*s*idx]; ai = a[2*s*idx+1];         \
    br = b[2*idx]; bi = b[2*idx+1];             \
    cr = ar*br - ai*bi;                         \
    ci = ar*bi + ai*br;                         \
  }

// DFT4*D_j implementation
static void DFT4_twiddle(double *Y, int s, int n, int j) {
  double t0, t1, t2, t3, t4, t5, t6, t7,
      X0, X1, X2, X3, X4, X5, X6, X7;
  double *Dj;
  // complex multiplications from D_N
  Dj = DN[n-2]+8*j;
  CMPLX_MULT(X0, X1, Y, Dj, 0, s);
  CMPLX_MULT(X2, X3, Y, Dj, 1, s);
  CMPLX_MULT(X4, X5, Y, Dj, 2, s);
  CMPLX_MULT(X6, X7, Y, Dj, 3, s);
  // operations from DFT4
  t0 = (X0 + X4);
  t1 = (X2 + X6);
  t2 = (X1 + X5);
  t3 = (X3 + X7);
  t4 = (X0 - X4);
  t5 = (X3 - X7);
  t6 = (X1 - X5);
  t7 = (X2 - X6);
  Y[0] = (t0 + t1);
  Y[1] = (t2 + t3);
  Y[4*s] = (t0 - t1);
  Y[4*s+1] = (t2 - t3);
  Y[2*s] = (t4 - t5);
  Y[2*s+1] = (t6 + t7);
  Y[6*s] = (t4 + t5);
  Y[6*s+1] = (t6 - t7);
}
