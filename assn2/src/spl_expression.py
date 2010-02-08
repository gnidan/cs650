#!/usr/bin/python

class SplExpression:
  expr_list = []

  def __init__(self, L):
    self.expr_list = L

  def generate_icode(self, input, output):
    pass

class Matrix:
  matrix = []
  rows   = 0
  cols   = 0

  def __init__(self, M):
    self.matrix = M
    self.rows = M.size()
    self.cols = M[0].size()

  # input and output are of type Vector
  def generate_icode(self, input, output):
    tmp_scalar = Scalar()

    do_i0    = Do(rows)
    assign_y = Assign( 0, output[do_i0.scalar] )
    do_i1    = Do(cols)
    
    mult_t   = Mult( matrix[ do_i0.scalar ] 

