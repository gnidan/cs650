#include <stdlib.h>
#include <math.h>

#define PI 3.141592653589793238462643383279

#define DBL_NE(A,B) (abs( (A) - (B) > 0.00001))

//All reals should equal 1, All imaginary values should be 0
void test0(double data[], size_t n) {
  for (size_t i = 0; i < 2*n; i++) {
    data[i] = (i==0);
  }
}

int check0(double data[], size_t n) {
  for (size_t i = 0; i < n; i++) {
    if (DBL_NE(data[2*i  ], 1))
      return 0;
    if (DBL_NE(data[2*i+1], 0))
      return 0;
  }
  return 1;
}

//data[0] should equal n
void test1(double data[], size_t n) {
  for (size_t i = 0; i < n; i++) {
    data[2*i  ] = 1;
    data[2*i+1] = 0;
  }
}

int check1(double data[], size_t n) {
  if (n > 0)
    if (DBL_NE(data[0], n))
      return 0;

  for (size_t i = 1; i < 2*n; i++) {
    if (DBL_NE(data[i], 0))
      return 0;
  }
  return 1;
}

//all sqrt( data[i].r^2 + data[i].i^2) should equal 1/n
void test2(double data[], size_t n) {
  for (size_t i = 0; i < 2*n; i++) {
    data[i] = (i==2);
  }
}

int check2(double data[], size_t n) {
  for (size_t i = 1; i < n; i++) {
    if (DBL_NE(data[2*i] * data[2*i] + data[2*i+1] * data[2*i+1], 1))
      return 0;
  }
  return 1;
}

void test3(double data[], size_t n) {
  for (size_t i = 0; i < 2*n; i++) {
    data[i] = i;
  }
}

void test4(double data[], size_t n) {
  for (size_t i = 0; i < n; i++) {
    data[2*i]   =  cos(10*(double)i/(double)n*2.0*PI);
    data[2*i+1] = -sin(10*(double)i/(double)n*2.0*PI);
  }
}
