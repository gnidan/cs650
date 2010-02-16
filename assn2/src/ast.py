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

import math
import cmath
import numbers
import symbol_collection as symbols
from options import Options

class Node:
    def __init__(self):
        raise NotImplementedError

    def optimize(self, symtab=None, options=None):
        '''Performs early optimizations on the AST such as Constant Folding'''
        pass #raise NotImplementedError #TODO Should be pass

    def evaluate(self, symtab=None, options=None):
        raise NotImplementedError

    def isConst(self,symtab=None):
        return False

    def __str__(self):
        return repr(self)

    def __repr__(self):
        '''prints the AST in an ATerm like format'''
        return self.__class__.__name__

class Formula(Node):
    def definition(self, symtab=None, options=None):
        if options.unroll:
            pass #TODO gen_code
        else:
            return symbols.Formula(self.value)

    def evaluate(self, symtab=None, options=None):
        print "Must implement Formula"


class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def evaluate(self, symtab=None, options=None):
        self.stmts.evaluate(symtab, options)

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

    def evaluate(self, symtab=None, options=None):
        for stmt in self.stmts:
            stmt.evaluate(symtab, options)

    def __repr__(self):
        return "StmtList(%s)" % (self.stmts)

    def __len__(self):
        return len(self.stmts)

#### NUMBERS ####
class Number(Node):
    pass

class Scalar(Number):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "%s" % (self.value)

    def isConst():
        return True

    def evaluate(self, symtab=None, options=None):
        return self.value

class Integer(Scalar):
    pass

class Double(Scalar):
    pass

class Pi(Double):
    def __init__(self):
        pass

    def evaluate(self, symtab=None, options=None):
        return math.pi

    def __repr__(self):
        return "pi"

class Complex(Number):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __repr__(self):
        return "Complex(%s, %s)" % (self.real, self.imaginary)

class ConstantError(ValueError):
    def __init__(self, msg):
        self.msg = "'%s' is not a constant" % (msg)

class Function(Node):
    def __init__(self, number):
        self.number = number

    def calc(self, arg, symtab=None):
        fname = self.__class__.__name__.lower()
        if isinstance(val, complex):
            module = cmath
        elif isinstance(val, numbers.Real):
            module = math
        else:
            raise ConstantError(val)
        if hasattr(module, fname):
                return getattr(module, fname)(arg)

    def optimize(self, symtab=None, options=None):
        return calc(self.number.evaluate(symtab, options))

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.number)

class Sin(Function): pass

class Cos(Function): pass

class Tan(Function): pass

class Log(Function): pass

class Exp(Function): pass

class Sqrt(Function): pass

class w(Function):
    def __init__(self, n, k=None):
        self.n = n
        self.k = k

    def __repr__(self):
        return "w(%s %s)" % (self.n, self.k)

##### Operators #####
class Operator:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.left, self.right)

class Add(Operator):
    pass

class Sub(Operator):
    pass

class Mul(Operator):
    pass

class Div(Operator):
    pass

class Mod(Operator):
    pass

class Neg(Operator):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.value)

##### 1.1 Predefined Matrix Constructors ######
class Constructor(Formula):
    def __init__(self):
        raise NotImplementedError

class MatrixRow(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values

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
        self.rows.insert(0, row)
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

class Index(Node):
    def __init__(self, start, stride, stop):
        self.start = start
        self.stride = stride
        self.stop = stop

    def __repr__(self):
        return "Index(%s, %s, %s)" % (self.start, self.stride, self.stop)

##### 1.2 Predefined Parametrized Matrices ######
class ParametrizedMatrix(Formula):
    pass

class F(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "(F %s)" % (self.n)

    def __icode__(self, out_v, in_v, symbol_table):
        out_loop = Do(n)
        in_loop =  Do(n)
        i0 = out_loop.var
        i1 = in_loop.var
        symbol_table.add_index(i0)
        symbol_table.add_index(i1)

        r  = symbol_table.get_new_int()
        f0 = symbol_table.get_new_scalar()
        f1 = symbol_table.get_new_scalar()

        icode = [
            out_loop,
            Assn(out_v[i0]),
            in_loop,
            Mult(r, i0, i1),
            Call(f0, W(n, r)),
            Mult(f1, f0, in_v[i1]),
            Mult(out_v[i0], out_v[i0], f1),
            EndDo(),
            EndDo()]
        return icode


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
    def __init__(self, mn, n, index=None):
        self.mn = mn
        self.n = n
        self.index = index

    def __repr__(self):
        return "(T %s %s %s)" % (self.mn, self.n, self.index)

class L(ParametrizedMatrix):
    def __init__(self, mn, n):
        self.mn = mn
        self.n = n

    def __repr__(self):
        return "(L %s %s)" % (self.mn, self.n)

##### 1.3 Predefined Matrix Operations ######
class Operation(Formula):
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
    def __init__(self, symbol, value, const=False):
        self.symbol = symbol
        self.value = value

    def isConst(self,symtab=None):
        return symtab.isConst(self.value)

    def evaluate(self, symtab=None, options=None):
        #Maybe this should call evaluate?
        print "Symbol: %s" % self.symbol
        print "Value: %s" % self.value
        symtab[self.symbol] = self.value.evaluate(symtab, options)

    def __repr__(self):
        return "Define(%s, %s)" % (self.symbol, self.value)

class Undefine(Assignment):
    def __init__(self, symbol, value):
        self.symbol = symbol

    def evaluate(self, symtab=None, options=None):
        del symtab[self.symbol]

    def __repr__(self):
        return "Undefine(%s)" % (self.symbol)

##### 2.2 Directive ######
class Directive(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symtab=None, options=None):
        options[self.__class__.__name__.lower()] = self.value.value()

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.value)

class SubName(Directive): pass

class DataType(Directive): pass

class CodeType(Directive): pass

class Optimize(Directive): pass

class Unroll(Directive): pass

class Verbose(Directive): pass

class Debug(Directive): pass

class Internal(Directive): pass

#### DirectiveParams ####
class DirectiveParam(Node):
    def __init__(self):
        pass

    def evaluate(self, symtab=None, options=None):
        return value()

    def value(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__

### Type ###
class Type(DirectiveParam):
    pass

class RealType(Type):
    def value(self):
        return numerics.Real

    def __repr__(self):
        return "real"

class ComplexType(Type):
    def value(self):
        return numerics.Complex

    def __repr__(self):
        return "complex"

### Flag ###
class Flag(DirectiveParam):
    pass

class On(Flag):
    def value(self):
        return True

class Off(Flag):
    def value(self):
        return False

### SubName ###
class Name(DirectiveParam):
    def __init__(self, value):
        self.value = value
    def value(self):
        return self.value

##### 2.3 Comments ######
class Comment(Node):
    def __init__(self, txt):
        self.txt = txt

    def evaluate(self, symtab=None, options=None):
        print "%s %s %s" % (options.lang.comment_begin(), self.txt, options.lang.comment_end())

    def __repr__(self):
        return "Comment(\"%s\")" % (self.txt)


class Intrinsic(Node):
    pass

class W(Intrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "W(%s %s)" % (self.m, self.k)

class WR(Intrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "WR(%s %s)" % (self.m, self.k)

class WI(Intrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "WI(%s %s)" % (self.m, self.k)

class TW(Intrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

    def __repr__(self):
        return "TW(%s %s %s)" % (self.m, self.n, self.k)

class TWR(Intrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

    def __repr__(self):
        return "TWR(%s %s %s)" % (self.m, self.n, self.k)

class TWI(Intrinsic):
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

    def __repr__(self):
        return "TWI(%s %s %s)" % (self.m, self.n, self.k)

class C(Intrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "C(%s %s)" % (self.m, self.k)

class S(Intrinsic):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def __repr__(self):
        return "S(%s %s)" % (self.m, self.k)

##### A.1 Errors #####
class AbstractClassError(NotImplementedError):
    def __init__(self, name):
        self.msg = "%s: Abstract class. Do not instantiate." % name
    def __str__(self):
        return self.msg
