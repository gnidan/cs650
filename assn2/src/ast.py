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
        return self.__name__

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

class MatrixRow(Constructor):
    def __init__(self, values):
        def self.n = len(values)
        self.values = values

    def __init__(self):
        def self.n = 0
        self.values = []

    def prepend(self, a):
        self.values.insert(0, a)
        self.n += 1

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.values)

class Matrix(Constructor):
    def __init__(self):
        self.m = 0
        self.n = 0
        self.rows = []

    def prepend(self, row):
        if len(self.rows) == 0:
            self.n = len(row)
        elif len(row) != self.n:
            raise ValueError("Invalid row size")
        self.rows.insert(0, rows)
        self.m += 1

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.rows)

class Diagonal(Constructor):
    def __init__(self, values):
        def self.n = len(values)
        self.values = values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.values)

class Permutation(Constructor):
    def __init__(self, values):
        def self.n = len(values)
        self.values = values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.values)

class RPermutation(Constructor):
    def __init__(self, values):
        def self.n = len(values)
        self.values = values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.values)

class SparseElement(Constructor):
    def __init__(self, i, j, a):
        self.i = i
        self.j = j
        self.a = a

    def __repr__(self):
        return "%s(%s %s %s)" % (self.__name__, self.i, self.j, self.a)

class Sparse(Constructor):
    def __init__(self, values):
        self.m = 0
        self.n = 0
        self.values = values
        #TODO calculate m and n from max values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "%s(%s)" % (self.__name__, self.values)

##### 1.2 Predefined Parametrized Matrices ######
class ParametrizedMatrix(Node):
    pass

class F(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "(%s %s)" % (self.__name__, self.n)

class I(ParametrizedMatrix):
    def __init__(self, n):
        self.m = n
        self.n = n

    def __init__(self, m, n):
        self.m = m
        self.n = n

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.m, self.n)

class J(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "(%s %s)" % (self.__name__, self.n)

class O(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "(%s %s)" % (self.__name__, self.n)

class T(ParametrizedMatrix):
    def __init__(self, mn, n):
        self.m = m
        self.n = n

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.m, self.n)

class L(ParametrizedMatrix):
    def __init__(self, mn, n):
        self.m = m
        self.n = n

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.m, self.n)

##### 1.3 Predefined Matrix Operations ######
class Operation(Node):
    pass

class Compose(Operation):
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.A, self.B)

class Tensor(Operation):
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.A, self.B)

class DirectSum(Operation):
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.A, self.B)

class Conjugate(Operation):
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.A, self.B)

class Scale(Operation):
    def __init__(self, a, B):
        self.a = a
        self.B = B

    def __repr__(self):
        return "(%s %s %s)" % (self.__name__, self.a, self.B)
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
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return "%s(%s)" % (self.__name__, self.symbol)

class Datatype(Directive):
    def __init__(self, t):
        self.t = t

    def __str__(self):
        return "%s(%s)" % (self.__name__, self.t)

class Codetype(Directive):
    def __init__(self, t):
        self.t = t

    def __str__(self):
        return "%s(%s)" % (self.__name__, self.t)

class Unroll(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __str__(self):
        return "%s(%s)" % (self.__name__, self.flag)

class Verbose(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __str__(self):
        return "%s(%s)" % (self.__name__, self.flag)

class Debug(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __str__(self):
        return "%s(%s)" % (self.__name__, self.flag)

class Internal(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __str__(self):
        return "%s(%s)" % (self.__name__, self.flag)

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
