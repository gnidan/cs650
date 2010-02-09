#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

ast.py

Contains all of the AST Node classes.
"""

import runtime

class MajorOrder:
    ROW=1
    COL=2

class OutputLanguage:

    
    def __init__(self):
        raise NotImplementedError('OutputLanguage: Base class. Do not instantiate')

class C99(OutputLanguage):
    def comment_begin():
        return "/*"

    def comment_end():
        return "*/"

    def index(rows, cols, i, j):
        return i * cols + j

    def major_order():
        return MajorOrder.ROW

class Node:
    def __init__(self):
        raise AbstractClassError(self.__class__)

    def evaluate(self, env, lang=C99):
        raise NotImplementedError('Node.evaluate: virtual method must be overridden')

    def __str__(self):
        return repr(self)

    def __repr__(self):
        '''prints the AST in an ATerm like format'''
        raise NotImplementedError('Node.__repr__: virtual method must be overridden')

class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

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

class Define(Node):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def __repr__(self):
        return "Define(%s, %s)" % (self.symbol, self.value)

class Integer(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Integer(%s)" % (self.value)

class Double(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Double(%s)" % (self.value)

class Complex(Node):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __repr__(self):
        return "Complex(%s)" % (self.real, self.imaginary)
    
##### 1.1 Predefined Matrix Constructors ######
class Constructor(Node):
    matrix     = []
    rows       = 0
    cols       = 0

    vector_var = None

    def __init__(self):
        raise AbstractClassError(self.__class__)

    def __store_matrix_vector__(self, symbol_table):
        # we're iterating over the matrix in the appropriate-major order and
        # storing that as a vector in the symbol table
        tmp        = NewTmp( rows * cols )
        vector_var = tmp.var
        iseq = [tmp]



class Matrix(Constructor):
    pass

class Diagonal(Constructor):
    pass

class Permutation(Constructor):
    pass

class RPermutation(Constructor):
    pass

class Sparse(Constructor):
    pass

##### 1.2 Predefined Parametrized Matrices ######
class ParametrizedMatrix(Node):
    pass

class I(ParametrizedMatrix):
    pass

class J(ParametrizedMatrix):
    pass

class O(ParametrizedMatrix):
    pass

class F(ParametrizedMatrix):
    pass

class L(ParametrizedMatrix):
    pass

class T(ParametrizedMatrix):
    pass

##### 1.3 Predefined Matrix Operations ######
class Operation(Node):
    pass

class Compose(Operation):
    pass

class Tensor(Operation):
    pass

class DirectSum(Operation):
    pass

class Conjugate(Operation):
    pass

class Scale(Operation):
    pass

##### 2.1 Assignment ######
class Assignment(Node):
    pass

class Define(Assignment):
    pass

class Undefine(Assignment):
    pass

##### 2.2 Directive ######
class Directive(Node):
    pass

class SubName(Directive):
    pass

class DataType(Directive):
    pass

class CodeType(Directive):
    pass

class Unroll(Directive):
    pass

class Verbose(Directive):
    pass

class Debug(Directive):
    pass

class Internal(Directive):
    pass

##### 2.3 Comments ######
class Comment(Node):
    pass

##### A.1 Errors #####
class AbstractClassError(NotImplementedError):
  def __init__(self, cls):
    self = NotImplementedError(cls.__name__ + ": Abstract class. Do not instantiate.")


