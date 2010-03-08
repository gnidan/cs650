#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

icode.py represents the icode

"""

class ICode(object):
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

  def __str__(self):
    return "dounroll(%s)" % (self.src1)

class Do(ICode):
  def __init__(self, src1):
    self.src1 = src1

  def __str__(self):
    return "do(%s)" % (self.src1)

class End(ICode):
  def __str__(self):
    return "end()"

class DefTmp(ICode):
  def __init__(self, src1):
    self.src1 = src1

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
    for s in self.stmts:
      s.evaluate(records, options)

  def __repr__(self):
    return "StmtList(%s)" % (self.stmts)

  def __len__(self):
    return len(self.stmts)

class Symbol(ICode):
  def __init__(self, symbol, subscript=None):
    self.var_type, self.index = symbol
    self.subscript = subscript

  def evaluate(self, records, **options):
    return records[self]

  def __repr__(self):
    if self.subscript == None:
      return "$%s%d" % (self.var_type, self.index)
    else:
      return "$%s%d[%s]" % (self.var_type, self.index, self.subscript)

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

  
