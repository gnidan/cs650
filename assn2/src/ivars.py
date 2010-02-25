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

import numbers

class Var:
  var_type = 'v'
  next_val = 0

  def __init__(self,val=None,name=None):
    self.val = None
    self.name = None

  def num(self):
    if self.val is None:
      return None
    elif isinstance(self.val, numbers.Number):
      return self.val
    else:
      return self.val.num()

  def __str__(self):
    if self.val:
      return str(self.val.num())
    if not self.name:
      self.name = "$%s%d" % (self.__class__.var_type, self.__class__.next_val)
      self.__class__.next_val += 1
    return self.name

class VarR(Var):
  var_type = 'r'
  next_val = 0

class VarF(Var):
  var_type = 'f'
  next_val = 0

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
  def __init__(self, vec, exp, stack=None):
    self.vec = vec
    self.exp = exp

    if stack:
      self.exp = self.idx(vec, exp, stack)

  def idx(self, vec, exp, stack):
    accum = exp[0]
    idxs = []
    e = exp[1:]
    for e,i in zip(exp[1:], stack):
      if isinstance(i.val, numbers.Integral):
        accum += e * i.val
      elif isinstance(i, Var):
        idxs.append("%d*%s" % (e, i.val))
      else:
        raise TypeError
    if not idxs:
      return accum
    idxs.append(str(accum))
    return '+'.join(idxs)

  def num(self):
    return self

  def __str__(self):
    return "Index(%s, %s)" % (self.vec, self.exp)

class Vec:
  var_type = 't'
  next_val = 0

  def __init__(self):
    self.name = None

  def __str__(self):
    if not self.name:
      self.name = "$%s%d" % (self.__class__.var_type, self.__class__.next_val)
      self.__class__.next_val += 1
    return self.name

  def idx(self, exp, stack):
    accum = exp[0]
    idxs = []
    e = exp[1:]
    for e,i,n in zip(exp[1:], stack, xrange(len(e)-1)):
      if isinstance(i.val, numbers.Integral):
        accum += e * i.val
      elif isinstance(i, Var):
        idxs.append("%d*%s" % (e, i.val))
      else:
        raise TypeError
    if not idxs:
      return accum
    idxs.append(str(accum))
    return '+'.join(idxs)

class VarIn(Vec):
  var_type = 'x'
  next_val = 0

class VarOut(Vec):
  var_type = 'y'
  next_val = 0
