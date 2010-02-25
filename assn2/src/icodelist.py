#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

icodelist.py represents the icodelist and optimizations

"""

import numbers

from intrinsics import *
from ivars import *
from symbol_collection import SymbolCollection

#TODO Need to keep track of a LoopIdx stack
#TODO Need to keep track of a Temp stack

def num(val):
  if isinstance(val, numbers.Number):
    return val
  else:
    return val.num()
  #raise NameError

def isnumeric(val):
  return isinstance(val, numbers.Number)

class ICodeList:
  def __init__(self, icode):
    self.icode = icode

  def varunroll(self, old, stack, varmap, outvar=False):
    if isinstance(old, numbers.Number):
      return old
    elif isinstance(old, Intrinsic):
      #n, k, mn
      if hasattr(old, 'n'):
        old.n = self.varunroll(old.n, stack, varmap, False)
      if hasattr(old, 'k'):
        old.k = self.varunroll(old.k, stack, varmap, False)
      if hasattr(old, 'mn'):
        old.mn = self.varunroll(old.mn, stack, varmap, False)
      return old
    elif isinstance(old, Vec):
      return old
    elif isinstance(old, Index):
      if isinstance(old.vec, Vec):
        if isinstance(old.exp, list):
          return Index(old.vec, old.exp, stack)
      return old
    elif isinstance(old, DoVar):
      raise TypeError
    elif isinstance(old, IRef):
      return stack[old.val].val
    #We want to do SSA. If we are an output variable, create
    #a new map. Otherwise we want to use our old value.
    elif outvar:
      varmap[old] = old.__class__(old.val, old.name)
      return varmap[old]
    elif old in varmap:
      return varmap[old]
    else:
      return old

  def unroll(self):
    unrolled = []
    stack = []
    varmap = {}
    i = 0
    while i < len(self.icode):
      inst = self.icode[i]

      #LOOPS
      if isinstance(inst, Do):
        stack.insert(0, DoVar(i,inst.src1))
      elif isinstance(inst, End):
        stack[0].val += 1
        #if < then we still have to loop, otherwise move on
        if stack[0].val < stack[0].n:
          i = stack[0].inst
        else:
          stack = stack[1:]

      elif isinstance(inst, Call):
        #TODO
        pass

      elif isinstance(inst, DefTmp):
        unrolled.append(DefTmp(inst.src1))
        #TODO

      #OPERATIONS
      elif isinstance(inst, OpICode):
        src1 = self.varunroll(inst.src1, stack, varmap, False)
        src2 = self.varunroll(inst.src2, stack, varmap, False)
        dest = self.varunroll(inst.dest, stack, varmap, True)
        unrolled.append(inst.__class__(src1, src2, dest))
      elif isinstance(inst, Copy):
        src1 = self.varunroll(inst.src1, stack, varmap, False)
        dest = self.varunroll(inst.dest, stack, varmap, True)
        unrolled.append(Copy(src1, dest))
      i+=1

    self.icode = unrolled

  def constprop(self):
    i = 0
    while i < len(self.icode):
      inst = self.icode[i]

      if isinstance(inst, OpICode):
        src1 = num(inst.src1)
        src2 = num(inst.src2)
        if src1:
          inst.src1 = src1
        if src2:
          inst.src2 = src2
        if isinstance(inst, Add):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 + src2
            self.icode[i] = None
          elif src1 == 0:
            inst.dest.val = src2
            self.icode[i] = None
          elif src2 == 0:
            inst.dest.val = src1
            self.icode[i] = None

        elif isinstance(inst, Sub):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 - src2
            self.icode[i] = None
          elif src2 == 0:
            inst.dest.val = src1
            self.icode[i] = None

        elif isinstance(inst, Mul):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 * src2
            self.icode[i] = None
          elif src1 == 0 or src2 == 0:
            inst.dest.val = 0
            self.icode[i] = None

        elif isinstance(inst, Div):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 / src2
            self.icode[i] = None
          elif src1 == 0:
            inst.dest.val = 0
            self.icode[i] = None
          elif src2 == 0:
            raise ZeroDivisionError

        elif isinstance(inst, Mod):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 % src2
            self.icode[i] = None
          elif src1 == 0:
            inst.dest.val = 0
            self.icode[i] = None
          elif src2 == 0:
            raise ZeroDivisionError

      elif isinstance(inst, Copy):
        src1 = num(inst.src1)
        if src1:
          inst.dest.val = src1.val

      i+=1

    #Remove any None placeholders
    self.icode = [i for i in self.icode if i]

#loop stack is just a list with the first element being the top
