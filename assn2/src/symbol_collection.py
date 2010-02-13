#!/usr/bin/python

class Variable:
  """Maintains the record for a particular variable in our symbol table"""
  access = []

  def __init__(self):

  def access(self, icode):
    """Record when a particular icode expression access this variable"""
    access.append(icode)

class Scalar(Variable):
  """Represents a scalar value"""
  value = 0

class Vector(Variable):
  """Represents a vector of scalars"""
  size = 0
  scalars = []

class Expression(Variable):
  """Represents an SPL Expression tree"""
  input_size = 0
  output_size = 0
  spl_expression = None

  def __init__(self, spl_expression):
    self.spl_expression = spl_expression

  def generate_icode(input, output):
    return spl_expression.generate_icode(input, output)

class SymbolTable:
  vectors = {}
  scalars = {}
  expressions = {}

  def define(name, spl_expression):
    expressions[name] = Expression(spl_expression)
    expressions.add(name)
