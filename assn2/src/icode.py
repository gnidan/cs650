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
  def simplify(self, records, options):
    if self.dest and isinstance(self.dest, Symbol):
      self.dest = self.dest.simplify(records, options)
    if self.src1 and isinstance(self.src1, Symbol):
      self.src1 = self.src1.simplify(records, options)
    if self.src2 and isinstance(self.src2, Symbol):
      self.src2 = self.src2.simplify(records, options)
    return self

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

  def simplify(self, records, options):
    return [s.simplify(records, options) for s in self.stmts]

  def __repr__(self):
    return "StmtList(%s)" % (self.stmts)

  def __len__(self):
    return len(self.stmts)

class Symbol:
  def __init__(self, symbol, subscript=None):
    self.var_type, self.index = symbol
    self.subscript = subscript

  def simplify(self, records, options):
    if self.subscript:
      for i in range(len(self.subscript)):
        if isinstance(self.subscript[i], Symbol):
          self.subscript[i] = self.subscript[i].simplify(records, options)
    return records[self]

  def __repr__(self):
    if self.subscript == None:
      return "$%s%s" % (self.var_type, self.index)
    else:
      return "$%s%s[%s]" % (self.var_type, self.index, self.subscript)
  
