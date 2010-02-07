#!/usr/bin/python

class Variable:
  pass


class SplOperation:
  def __init__(self, *args):
    self.args = args

  def generate_icode(self, input, output):
    return []

class Compose(SplOperation):
  def __init__(self, A, B):
    self.args = [A, B]

  def generate_icode(self, input, output):
    tmp = Variable()
    iseq = B.generate_icode(input, tmp)
    iseq.append( A.generate_icode(tmp, output)
    return iseq

class ICode:
  def __init__(self, op, src1, src2, dest):
    self.inst = op, src1, src2, dest

  def op(self):
    return self.inst[0]

  def src1(self):
    return self.inst[1]

  def src2(self):
    return self.inst[2]

  def dest(self):
    return self.inst[3]

