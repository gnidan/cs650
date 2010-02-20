#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

icode_vars.py

Contains all of the variable types referenced at various stages of ICode.
"""

global_var_numbers = {'r' : 0, 'f' : 0, 'x':0, 'y':0}


class Var:
  def __init__(self,val=None,name=None):
    self.val = None
    self.name = None

  def __int__(self):
    return self.val

  def __str__(self):
    return "%s" % (self.__class__.__name__)

class VarR(Var):
  def __str__(self):
    if self.name is None:
      self.name = global_var_numbers['r']
      global_var_numbers['r'] += 1
    return "$r%d" % (self.name)

class VarF(Var):
  def __str__(self):
    if self.name is None:
      self.name = global_var_numbers['f']
      global_var_numbers['f'] += 1
    return "$f%d" % (self.name)

class DoVar(Var):
  """This is used in Do Loops to indicate the current loop value"""
  def __init__(self,inst,n,val=0):
    self.inst = inst #The instruction this variable is associated with.
    self.n = n # The value that this variable goes up to
    self.val = val #The present value during a particular unrolling step

  def __str__(self):
    return "DoVar(val=%d, n=%d, inst=%d)" % (self.val, self.n, self.inst)

class IRef(Var):
  """This is just a reference to a variable $i0, $i1 ... """
  def __init__(self,val):
    self.val = val

  def __str__(self):
    return "$i%d" % (self.val)

class Index:
  """This is used to store the index in icode."""
  def __init__(self, vec, exp):
    self.vec = vec
    self.exp = exp

  def __str__(self):
    return "Index(%s, %s)" % (self.vec, self.exp)

class Vec:
  def __init__(self):
    self.name = None

  def idx(self, exp, i_stack):
    accum = exp[0]
    idxs = []
    e = exp[1:]
    for e,i,n in zip(exp[1:], i_stack, xrange(len(e)-1)):
      if isinstance(i, numbers.Integral):
        accum += e * i
      elif isinstance(i, Var):
        idxs.append("%d*%s", e, i.name)
      else:
        raise TypeError
    if not idxs:
      return accum
    idxs.append(str(accum))
    return '+'.join(idxs)

class VarIn(Vec):
  def __str__(self):
    if self.name is None:
      self.name = global_var_numbers['x']
      global_var_numbers['x'] += 1
    return "$x%d" % (self.name)

class VarOut(Vec):
  def __str__(self):
    if self.name is None:
      self.name = global_var_numbers['y']
      global_var_numbers['y'] += 1
    return "$y%d" % (self.name)
