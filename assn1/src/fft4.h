#ifndef _FFT4_H_
#define _FFT4_H_

// recursive radix-4 DFT implementation

// compute the exponent
#include <math.h>
#define log4(N) (int)(log(N)/log(4))

// top-level call to DFT function
#define DFT(N, Y, X) DFT_rec(N, log4(N), Y, X, 1)

// recursive radix-4 DFT function
// N: problem size
// Y: output vector
// X: input vector
// s: stride to access X
void DFT_rec(int N, int n, double *Y, double *X, int s);

// recursive radix-4 DFT function with buffering
// N: problem size
// Y: output vector
// X: input vector
// s: stride to access X
// th: threshold size to stop buffering
void DFT_buf_rec(int N, int n, double *Y, double *X, int s, int th);

void init_DFT(int N);
void destroy_DFT();

#endif /* _FFT4_H_ */
