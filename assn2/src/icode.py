#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

icode.py represents the icode

"""

import copy

class ICode(object):
  def evaluate(self, records, options):
    new = copy.copy(self)
    
    if self.dest:
      new.dest = self.dest.evaluate(records, options)
    if self.src1:
      new.src1 = self.src1.evaluate(records, options)
    if self.src2:
      new.src2 = self.src2.evaluate(records, options)

    return new

  def __repr__(self):
    return str(self)

class OpICode(ICode):
  """This is used to better categorize all of the Arithmetic Operation
  instructions"""
  pass

class Add(OpICode):
  op = '+'
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __str__(self):
    return "add(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Sub(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __str__(self):
    return "sub(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Mul(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __str__(self):
    return "mul(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Div(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __str__(self):
    return "div(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Mod(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __str__(self):
    return "mod(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Copy(ICode):
  def __init__(self, src1, dest):
    self.src1 = src1
    self.src2 = None
    self.dest = dest

  def __str__(self):
    return "copy(%s, %s)" % (self.src1, self.dest)

class Call(ICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __str__(self):
    return "call(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class DoUnroll(ICode):
  def __init__(self, src1):
    self.src1 = src1
    self.src2 = None
    self.dest = None

  def __str__(self):
    return "dounroll(%s)" % (self.src1)

class Do(ICode):
  def __init__(self, src1):
    self.src1 = src1
    self.src2 = None
    self.dest = None

  def __str__(self):
    return "do(%s)" % (self.src1)

class End(ICode):
  def __init__(self):
    self.src1 = None
    self.src2 = None
    self.dest = None

  def __str__(self):
    return "end()"

class DefTmp(ICode):
  def __init__(self, src1):
    self.src1 = src1
    self.src2 = None
    self.dest = None

  def __str__(self):
    return "deftmp(%s)" % (self.src1)

class StmtList(ICode):
  def __init__(self, stmt=None):
    if stmt is None:
      self.stmts = []
    else:
      self.stmts = [stmt]
      
  def prepend(self, stmt):
    self.stmts.insert(0, stmt)
        
  def flatten(self):
    new_stmts = []
    for stmt in self.stmts:
      if issubclass(stmt.__class__, StmtList):
        stmt.flatten()
        new_stmts.extend(stmt.stmts)
      else:
        new_stmts.append(stmt)
        
      self.stmts = new_stmts

  def evaluate(self, records, options):
    return [s.evaluate(records, options) for s in self.stmts]

  def __repr__(self):
    return "StmtList(%s)" % (self.stmts)

  def __len__(self):
    return len(self.stmts)

class Symbol(ICode):
  def __init__(self, symbol, subscript=None, dot=None):
    self.var_type, self.index = symbol
    self.subscript = subscript
    self.dot = dot

  def evaluate(self, records, options):
    return records[self]

  def __repr__(self):
    if self.subscript == None:
      return "$%s%s" % (self.var_type, self.index)
    else:
      return "$%s%s[%s]" % (self.var_type, self.index, self.subscript)

class Subscript(ICode):
  def __init__(self, index, *multiplicands):
    self.index = index
    self.multiplicands = multiplicands

  def __repr__(self):
    r = repr(self.index)
    for m in self.multiplicands:
      r += " "
      r += repr(m)
    return r

class Index(ICode):
  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return repr(self.value)

class Range(Index):
  def __init__(self, start, stride, end):
    self.start = start
    self.stride = stride
    self.end = end

  def __repr__(self):
    return "%s:%s:%s" % (repr(self.start), repr(self.stride), repr(self.end))

  
