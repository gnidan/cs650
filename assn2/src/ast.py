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
        raise NotImplementedError('Node: Base class. Do not instantiate')

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
    
#### NUMBERS ####
class Number(Node):
    pass
    
class Scalar(Number):
    pass

class Integer(Scalar):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Integer(%s)" % (self.value)

class Double(Scalar):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Double(%s)" % (self.value)

class Complex(Number):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __repr__(self):
        return "Complex(%s)" % (self.real, self.imaginary)


class Function(Node):
    pass

class Sin(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.number)

class Cos(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.number)

class Tan(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.number)
    
class Log(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.number)

class Exp(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.number)

class Sqrt(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.number)

class Pi(Function):
    def __init__(self):
        pass

    def __repr__(self):
        return "%s" % (self.__name__)

##### Operators #####
class Add(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s)" % (self.__name, self.left, self.right)

class Sub(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s)" % (self.__name, self.left, self.right)


class Mul(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s)" % (self.__name, self.left, self.right)


class Div(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s)" % (self.__name, self.left, self.right)


class Mod(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s)" % (self.__name, self.left, self.right)

class Neg(Function):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "%s(%s)" % (self.__name, self.value)

##### 1.1 Predefined Matrix Constructors ######
class Constructor(Node):
    pass

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
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def __repr__(self):
        return "%s(%s, %s)" % (self.__name__, self.symbol, self.value)

class Undefine(Assignment):
    def __init__(self, symbol, value):
        self.symbol = symbol

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.symbol)

##### 2.2 Directive ######
class Directive(Node):
    pass

class Subname(Directive):
    pass

class Datatype(Directive):
    pass

class Codetype(Directive):
    pass

class Unroll(Directive):
    pass

class Verbose(Directive):
    pass

class Debug(Directive):
    pass

class Internal(Directive):
    pass

#### Type ####
class Type(Node):
    pass

class RealType(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "real"

class ComplexType(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "complex"

#### Flag ####
class Flag(Node):
    pass

class On(Flag):
    def __init__(self):
        pass

    def __repr__(self):
        return self.__name__

class Off(Flag):
    def __init__(self):
        pass

    def __repr__(self):
        return self.__name__

##### 2.3 Comments ######
class Comment(Node):
    def __init__(self, txt):
        self.txt = txt

    def __repr__(self):
        return "%s(%s)", self.__name__, self.txt
