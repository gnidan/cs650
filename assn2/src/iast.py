#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

iast.py

Contains all of the AST Node classes for ICode.
"""

import math
import cmath

from symbols import ICodeRecordSet

class Node:
    dest = None
    src1 = None
    src2 = None

    def __init__(self):
        raise AbstractClassError('Node')

    def evaluate(self, records, **options):
      if self.dest:
        self.dest = self.dest.evaluate(records, **options)
      if self.src1:
        self.src1 = self.src1.evaluate(records, **options)
      if self.src2:
        self.src2 = self.src2.evaluate(records, **options)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        '''prints the AST in an ATerm like format'''
        raise NotImplementedError

class ICode(Node):
    def __init__(self, stmts):
      self.stmts = stmts

    def evaluate(self, **options):
      # options should include input_size and output_size
      records = ICodeRecordSet(**options)
      options["program"] = self

      self.stmts.flatten()
      self.stmts.evaluate(records, **options)

    def __repr__(self):
      return "Program(%s)" % (self.stmts)

class StmtList(Node):
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

    def evaluate(self, records, **options):
      for s in self.stmts:
        s.evaluate(records, **options)

    def __repr__(self):
        return "StmtList(%s)" % (self.stmts)

    def __len__(self):
        return len(self.stmts)

class Add(Node):
  def __init__(self, dest, src1, src2):
    self.dest = dest
    self.src1 = src1
    self.src2 = src2

  def __repr__(self):
    return "Add(%s = %s + %s)" % (self.dest, self.src1, self.src2)

class Subtract(Node):
  def __init__(self, dest, src1, src2):
    self.dest = dest
    self.src1 = src1
    self.src2 = src2

  def __repr__(self):
    return "Subtract(%s = %s - %s)" % (self.dest, self.src1, self.src2)

class Multiply(Node):
  def __init__(self, dest, src1, src2):
    self.dest = dest
    self.src1 = src1
    self.src2 = src2

  def __repr__(self):
    return "Multiply(%s = %s * %s)" % (self.dest, self.src1, self.src2)

class Divide(Node):
  def __init__(self, dest, src1, src2):
    self.dest = dest
    self.src1 = src1
    self.src2 = src2

  def __repr__(self):
    return "Divide(%s = %s / %s)" % (self.dest, self.src1, self.src2)

class Modulus(Node):
  def __init__(self, dest, src1, src2):
    self.dest = dest
    self.src1 = src1
    self.src2 = src2

  def __repr__(self):
    return "Modulus(%s = %s \% %s)" % (self.dest, self.src1, self.src2)

class Assign(Node):
  def __init__(self, dest, src1):
    self.dest = dest
    self.src1 = src1

  def __repr__(self):
    return "Assign(%s = %s)" % (self.dest, self.src1)

class Call(Node):
  def __init__(self, dest, src1, src2=None):
    self.dest = dest
    self.src1 = src1
    self.src2 = src2

  def __repr__(self):
    if self.src2 == None:
      return "%s = Call(%s)" % (self.dest, self.src1)
    else:
      return "%s = Call(%s(%s))" % (self.dest, self.src1, self.src2)

class Do(Node):
  def __init__(self, src1, stmt_list, unroll=False):
    self.src1 = src1
    self.stmts = stmt_list
    if unroll:
      self = self.unroll() 
  
  def unroll(self):
    return self

  def __repr__(self):
    return "Do(%s, %s)" % (self.src1, self.stmts)

class NewTmp(Node):
  def __init__(self, src1):
    self.src1 = src1

  def __repr__(self):
    return "NewTmp(%s)" % self.src1

class Index(Node):
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

class Subscript(Node):
  def __init__(self, index, *multiplicands):
    self.index = index
    self.multiplicands = multiplicands

  def __repr__(self):
    r = repr(self.index)
    for m in self.multiplicands:
      r += " "
      r += repr(m)
    return r

class Symbol(Node):
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

class Comment(Node):
  def __init__(self, comment):
    self.comment = comment

  def __repr__(self):
    return "Comment(\"%s\")" % self.comment

##### Record Keeping #####
