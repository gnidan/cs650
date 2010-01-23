#ifndef _TEST_H_
#define _TEST_H_

#include <stdlib.h>

typedef void(*test_func)(double data[], size_t n);
typedef int(*check_func)(double data[], size_t n);

void test0(double data[], size_t n);
void test1(double data[], size_t n);
void test2(double data[], size_t n);
void test3(double data[], size_t n);
void test4(double data[], size_t n);

int check0(double data[], size_t n);
int check1(double data[], size_t n);
int check2(double data[], size_t n);
int check3(double data[], size_t n);
int check4(double data[], size_t n);

struct test_func_t {
  test_func func;
  check_func check;
  char *name;
  char *desc;
};

static const size_t num_test_funcs = 5;
static const struct test_func_t test_funcs[] = {
  {test0, check0, "test0", ""},
  {test1, check1, "test1", ""},
  {test2, check2, "test2", ""},
  {test3, NULL,   "test3", ""},
  {test4, NULL,   "test4", ""},
};

#endif /* _TEST_H_ */
