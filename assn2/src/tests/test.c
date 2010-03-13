#include <complex.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "out.c"


#define M_PI 3.14159265358979323846


/**
 * @brief Compare the observed column of the DFT matrix with the actual column.
 *
 * @param col     The observed column.
 * @param col_num Which column in the matrix we're looking at.
 * @param size    The size of the DFT matrix.
 *
 * @return 1 if the columns match, 0 otherwise
 */
unsigned int compare_col (complex double *col, size_t col_num, size_t size)
{
  static const double TOL = 0.001;
  double omega_r, omega_i, o_r, o_i, a, b;
  unsigned int i;

  /* 0th column should be all 1.0 + 0.0 * I */
  if ( col_num == 0 )
    for ( i = 0; i < size; ++i )
      if ( (fabs (creal(col[i]) - 1.0) > TOL) || 
	   (fabs (cimag(col[i]) - 0.0) > TOL) )
	return 0;
  
 
  /* 0th row should always be 1.0 + 0.0 * I */
  if ( (fabs (creal(col[0]) - 1.0) > TOL ) ||
       (fabs (cimag(col[0]) - 0.0) > TOL ) )
    return 0;

  
  /* calculate the primitive nth root of unity */
  omega_r = cos (2 * M_PI / (float) size);
  omega_i = sin (2 * M_PI / (float) size);
  
  /* set o_r and o_i to represents omeaga^col_num */
  o_r = 1.0;
  o_i = 0.0;
  for ( i = 0; i < col_num; ++i )
    {
      a = o_r;
      b = o_i;
      o_r = a * omega_r - b * omega_i;
      o_i = a * omega_i + b * omega_r;
    }

  /* now, o_r + o_i * i is omega^col_num */
  omega_r = o_r;
  omega_i = o_i;
  for ( i = 1; i < size; ++i )
    {
      if ( (fabs (creal(col[i]) - o_r) > TOL) ||
	   (fabs (cimag(col[i]) - o_i) > TOL) )
	return 0;
      a = o_r;
      b = o_i;
      o_r = a * omega_r - b * omega_i;
      o_i = a * omega_i + b * omega_r;
    }
  return 1;
}


/**
 * @brief Verify that the DFT of the given size is correct.
 *
 * @param s    The size of the DFT being computed.
 * @param fptr A pointer to the function which computes the DFT of the given
 *             size.
 *
 * @return 1 if the function is correct, 0 otherwise
 */
unsigned int test_func(size_t s, 
		       void (*fptr)(complex double *, complex double *)) {
  complex double *x = malloc(sizeof(complex double) * s);
  complex double *y = malloc(sizeof(complex double) * s);

  for (size_t col = 0; col < s; col++) {
    for (size_t i = 0; i < s; i++) {
      x[i] = col==i;
      y[i] = 0;
    }

    fptr(y, x);
    if ( !compare_col (y, col, s) )
      return 0;
/*  printf("col = %zu\n", col); */
/*     for (size_t i = 0; i < s; i++) { */
/*       printf("%f + %f i\n", creal(y[i]), cimag(y[i])); */
/*     } */
/*     printf("\n"); */
  }
 /*  printf("\n\n"); */
  return 1;
}

int main(int argc, char *argv[]) {

  /* printf("F(2)\n"); */
  /* test_func(2, func_2); */

  /* printf("F(3)\n"); */
  /* test_func(3, func_3); */

  /* printf("F(4)\n"); */
  /* test_func(4, func_4); */

  /* printf("F(5)\n"); */
  /* test_func(5, func_5); */

  /* printf("F(6)\n"); */
  /* test_func(6, func_6); */

  /* printf("F(7)\n"); */
  /* test_func(7, func_7); */

  /* printf("F(8)\n"); */
  /* test_func(8, func_8); */

  /* printf("F(8)\n"); */
  /* test_func(8, func_8); */

/*   printf("F(64) -- "); */
/*   if ( !test_func(64, func) ) */
/*     printf ("PASSSED\n"); */

  printf ("F(64) -- %s\n", test_func (64, func) ? "PASSED" : "FAILED");

  /* printf("F(9)\n"); */
  /* test_func(9, func_9); */

  /* printf("F(10)\n"); */
  /* test_func(10, func_10); */

  /* printf("F(11)\n"); */
  /* test_func(11, func_11); */

  /* printf("F(12)\n"); */
  /* test_func(12, func_12); */

  /* printf("F(13)\n"); */
  /* test_func(13, func_13); */

  /* printf("F(14)\n"); */
  /* test_func(14, func_14); */

  /* printf("F(15)\n"); */
  /* test_func(15, func_15); */

  /* printf("F(16)\n"); */
  /* test_func(16, func_16); */

  /* printf("F(17)\n"); */
  /* test_func(17, func_17); */

  /* printf("F(18)\n"); */
  /* test_func(18, func_18); */

  /* printf("F(18)\n"); */
  /* test_func(18, func_18); */

  /* printf("F(19)\n"); */
  /* test_func(19, func_19); */

  /* printf("F(20)\n"); */
  /* test_func(20, func_20); */

  /* printf("F(21)\n"); */
  /* test_func(21, func_21); */

  /* printf("F(22)\n"); */
  /* test_func(22, func_22); */

  /* printf("F(23)\n"); */
  /* test_func(23, func_23); */

  /* printf("F(24)\n"); */
  /* test_func(24, func_24); */

  /* printf("F(25)\n"); */
  /* test_func(25, func_25); */

  /* printf("F(26)\n"); */
  /* test_func(26, func_26); */

  /* printf("F(27)\n"); */
  /* test_func(27, func_27); */

  /* printf("F(28)\n"); */
  /* test_func(28, func_28); */

  /* printf("F(28)\n"); */
  /* test_func(28, func_28); */

  /* printf("F(29)\n"); */
  /* test_func(29, func_29); */

  /* printf("F(30)\n"); */
  /* test_func(30, func_30); */

  /* printf("F(31)\n"); */
  /* test_func(31, func_31); */

  /* printf("F(32)\n"); */
  /* test_func(32, func_32); */

  /* printf("F(33)\n"); */
  /* test_func(33, func_33); */

  /* printf("F(34)\n"); */
  /* test_func(34, func_34); */

  /* printf("F(35)\n"); */
  /* test_func(35, func_35); */

  /* printf("F(36)\n"); */
  /* test_func(36, func_36); */

  /* printf("F(37)\n"); */
  /* test_func(37, func_37); */

  /* printf("F(38)\n"); */
  /* test_func(38, func_38); */

  /* printf("F(38)\n"); */
  /* test_func(38, func_38); */

  /* printf("F(39)\n"); */
  /* test_func(39, func_39); */

  /* printf("F(30)\n"); */
  /* test_func(30, func_30); */

  /* printf("F(31)\n"); */
  /* test_func(31, func_31); */

  /* printf("F(32)\n"); */
  /* test_func(32, func_32); */

  /* printf("F(33)\n"); */
  /* test_func(33, func_33); */

  /* printf("F(34)\n"); */
  /* test_func(34, func_34); */

  /* printf("F(35)\n"); */
  /* test_func(35, func_35); */

  /* printf("F(36)\n"); */
  /* test_func(36, func_36); */

  /* printf("F(37)\n"); */
  /* test_func(37, func_37); */

  /* printf("F(38)\n"); */
  /* test_func(38, func_38); */

  /* printf("F(38)\n"); */
  /* test_func(38, func_38); */

  /* printf("F(39)\n"); */
  /* test_func(39, func_39); */

  return 0;
}
