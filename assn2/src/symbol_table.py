#!/usr/bin/python

class SymbolTable:
  vectors = {}
  scalars = {}
  expressions = {}

  def define(name, spl_expression):
    expressions[name] = Expression(spl_expression)
    expressions.add(name)

