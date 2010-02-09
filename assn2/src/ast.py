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

    def evaluate(self, env, options={'wsign' : 1, 'lang' : C99} ):
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
        return "Sin(%s)" % (self.number)

class Cos(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "Cos(%s)" % (self.number)

class Tan(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "Tan(%s)" % (self.number)

class Log(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "Log(%s)" % (self.number)

class Exp(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "Exp(%s)" % (self.number)

class Sqrt(Function):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "Sqrt(%s)" % (self.number)

class Pi(Function):
    def __init__(self):
        pass

    def __repr__(self):
        return "pi"

class w(Function):
    def __init__(self, n, k=None):
        self.n = n
        self.k = k

    def __repr__(self):
        return "w(%s %s)" % (self.n, self.k)

##### Operators #####
class Add(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Add(%s, %s)" % (self.left, self.right)

class Sub(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Sub(%s, %s)" % (self.left, self.right)


class Mul(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Mul(%s, %s)" % (self.left, self.right)


class Div(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Div(%s, %s)" % (self.left, self.right)


class Mod(Function):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Mod(%s, %s)" % (self.left, self.right)

class Neg(Function):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Neg(%s)" % (self.value)

##### 1.1 Predefined Matrix Constructors ######
class Constructor(Node):
    pass

class MatrixRow(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values

    def __init__(self):
        self.n = 0
        self.values = []

    def prepend(self, a):
        self.values.insert(0, a)
        self.n += 1

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "MatrixRow(%s)" % (self.values)

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
        return "Matrix(%s)" % (self.rows)

class Diagonal(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "Diagonal(%s)" % (self.values)

class Permutation(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "Permutation(%s)" % (self.values)

class RPermutation(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "RPermutation(%s)" % (self.values)

class SparseElement(Constructor):
    def __init__(self, i, j, a):
        self.i = i
        self.j = j
        self.a = a

    def __repr__(self):
        return "SparesElement(%s %s %s)" % (self.i, self.j, self.a)

class Sparse(Constructor):
    def __init__(self, values):
        self.m = 0
        self.n = 0
        self.values = values
        #TODO calculate m and n from max values

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "Sparse(%s)" % (self.values)

##### 1.2 Predefined Parametrized Matrices ######
class ParametrizedMatrix(Node):
    pass

class F(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "(F %s)" % (self.n)

class I(ParametrizedMatrix):
    def __init__(self, m, n=None):
        self.m = m
        self.n = n

    def __repr__(self):
        return "(I %s %s)" % (self.m, self.n)

class J(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "(J %s)" % (self.n)

class O(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "(O %s)" % (self.n)

class T(ParametrizedMatrix):
    def __init__(self, mn, n):
        self.mn = mn
        self.n = n

    def __repr__(self):
        return "(T %s %s)" % (self.mn, self.n)

class L(ParametrizedMatrix):
    def __init__(self, mn, n):
        self.mn = mn
        self.n = n

    def __repr__(self):
        return "(L %s %s)" % (self.mn, self.n)

##### 1.3 Predefined Matrix Operations ######
class Operation(Node):
    pass

class Compose(Operation):
    def __init__(self, formulas):
        self.formulas = formulas

    def __repr__(self):
        return "Compose(%s)" % (self.formulas)

class Tensor(Operation):
    def __init__(self, formulas):
        self.formulas = formulas

    def __repr__(self):
        return "Tensor(%s)" % (self.formulas)


class DirectSum(Operation):
    def __init__(self, formulas):
        self.formulas = formulas

    def __repr__(self):
        return "DirectSum(%s)" % (self.formulas)

class Conjugate(Operation):
    def __init__(self, A, P):
        self.A = A
        self.P = P

    def __repr__(self):
        return "Conjugate(%s %s)" % (self.A, self.P)

class Scale(Operation):
    def __init__(self, a, A):
        self.a = a
        self.A = A

    def __repr__(self):
        return "Scale(%s %s)" % (self.a, self.A)

##### 2.1 Assignment ######
class Assignment(Node):
    pass

class Define(Assignment):
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def __repr__(self):
        return "Define(%s, %s)" % (self.symbol, self.value)

class Undefine(Assignment):
    def __init__(self, symbol, value):
        self.symbol = symbol

    def __repr__(self):
        return "Undefine(%s)" % (self.symbol)

##### 2.2 Directive ######
class Directive(Node):
    pass

class SubName(Directive):
    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return "SubName(%s)" % (self.symbol)

class DataType(Directive):
    def __init__(self, t):
        self.t = t

    def __repr__(self):
        return "DataType(%s)" % (self.t)

class CodeType(Directive):
    def __init__(self, t):
        self.t = t

    def __repr__(self):
        return "CodeType(%s)" % (self.t)

class Optimize(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __repr__(self):
        return "Optimize(%s)" % (self.flag)

class Unroll(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __repr__(self):
        return "Unroll(%s)" % (self.flag)

class Verbose(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __repr__(self):
        return "Verbose(%s)" % (self.flag)

class Debug(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __repr__(self):
        return "Debug(%s)" % (self.flag)

class Internal(Directive):
    def __init__(self, flag):
        self.flag = flag

    def __repr__(self):
        return "Inernal(%s)" % (self.flag)

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
        return "on"

class Off(Flag):
    def __init__(self):
        pass

    def __repr__(self):
        return "off"

##### 2.3 Comments ######
class Comment(Node):
    def __init__(self, txt):
        self.txt = txt

    def __repr__(self):
        return "Comment(%s)" % (self.txt)


class Intrinsic(Node):
    pass

class W(Instrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "W(%s %s)" % (self.m, self.k)

class WR(Instrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "WR(%s %s)" % (self.m, self.k)

class WI(Instrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "WI(%s %s)" % (self.m, self.k)

class TW(Instrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

    def __repr__(self):
        return "TW(%s %s %s)" % (self.m, self.n, self.k)

class TWR(Instrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

    def __repr__(self):
        return "TWR(%s %s %s)" % (self.m, self.n, self.k)

class TWI(Instrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

    def __repr__(self):
        return "TWI(%s %s %s)" % (self.m, self.n, self.k)

class C(Instrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "C(%s %s)" % (self.m, self.k)

class S(Instrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "S(%s %s)" % (self.m, self.k)
