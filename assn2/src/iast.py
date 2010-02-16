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
class Node:
    def __init__(self):
        raise AbstractClassError('Node')

    def evaluate(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return repr(self)

    def __repr__(self):
        '''prints the AST in an ATerm like format'''
        raise NotImplementedError

class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def evaluate(self, *args, **kwargs):
        raise NotImplementedError

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
  def __init__(self, src1, stmt_list):
    self.src1 = src1
    self.stmts = stmt_list

  def __repr__(self):
    return "Do(%s, %s)" % (self.src1, self.stmts)

class NewTmp(Node):
  def __init__(self, src1):
    self.src1 = src1

  def __repr__(self):
    return "NewTmp(%s)" % self.src1

class Symbol(Node):
  def __init__(self, symbol, subscript=None):
    self.symbol = symbol
    self.subscript = subscript

  def __repr__(self):
    if self.subscript == None:
      return "$%s" % self.symbol
    else:
      return "$%s[%s]" % (self.symbol, self.subscript)

class Comment(Node):
  def __init__(self, comment):
    self.comment = comment

  def __repr__(self):
    return "Comment(\"%s\")" % self.comment
