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
import templates
import types
import symbol_collection as symbols
from options import Options
from icodelist import ICodeList

class Node(object):
    def __init__(self):
        raise NotImplementedError

    def simplify(self, symtab):
        '''Performs simplification of the AST. Propagates defines, folds constants, etc.'''
        print "OPTIMIZING: %s" % (self.__class__.__name__)
        return self

    def evaluate(self, options):
        print self.__class__.__name__
        raise NotImplementedError

    def isConst(self,symtab=None):
        return False

    def __str__(self):
        return repr(self)

    def __repr__(self):
        '''prints the AST in an ATerm like format'''
        return self.__class__.__name__

class Formula(Node):
    def __init__(self, values):
        self.values = values
        self._nx = None
        self._ny = None

    #This is absolutely horrible
    def nx(self):
        if self._nx is None:
            pass

    def ny(self):
        if self._ny is None:
            pass

    def func(self):
        if hasattr(templates, self.__class__.__name__):
            f = getattr(templates, self.__class__.__name__, None)
            if not isinstance(f, types.FunctionType):
                raise TypeError
            return f
        raise NotImplementedError("Must implement Formula '%s'" % (self.__class__.__name__))


    def func(self):
        if hasattr(templates, self.__class__.__name__):
            f = getattr(templates, self.__class__.__name__, None)
            if not isinstance(f, types.FunctionType):
                raise TypeError
            return f
        raise NotImplementedError("Must implement Formula '%s'" % (self.__class__.__name__))

    def size_func(self):
        name = "%s_size" % (self.__class__.__name__)
        if hasattr(templates, name):
            f = getattr(templates, name, None)
            if not isinstance(f, types.FunctionType):
                raise TypeError
            return f
        raise NotImplementedError("Must implement size function for '%s'" % (self.__class__.__name__))

    def evaluate(self, options):
        return ICodeList(self.func()(*tuple(self.values)))

    def __call__(self, x, y):
        print "Calling: %s size: %s %s" % (self.__class__.__name__, self.nx, self.ny)
        self.il = ICodeList(self.func()(*tuple(self.values),x=x, y=y))
        return self.il

    def __init__(self, values):
        self.values = values
        self.nx, self.ny = self.size_func()(*tuple(self.values))

    def simplify(self, symtab):
        self.values = [ i.simplify(symtab) for i in self.values ]
        self.values = [ i for i in self.values if i ]
        return self

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.values)

class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def evaluate(self, options):
        return self.stmts.evaluate(options)

    def simplify(self, symtab):
        self.stmts = self.stmts.simplify(symtab)
        return self

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

    def evaluate(self, options):
        return [s.evaluate(options) for s in self.stmts]

    def simplify(self, symtab):
        self.stmts = [ i.simplify(symtab) for i in self.stmts ]
        self.stmts = [ i for i in self.stmts if i ]
        return self

    def __repr__(self):
        return "StmtList(%s)" % (self.stmts)

    def __len__(self):
        return len(self.stmts)

#### NUMBERS ####
class Number(Node):
    pass

class Scalar(Number):
    def __init__(self, val):
        self.val = val

    def isConst(self, symtab=None):
        return True

    def value(self):
        return self.val

    def simplify(self, symtab):
        return self.value()

    def evaluate(self, options):
        return self.value()

    def __repr__(self):
        return "%s" % (self.val)

class Integer(Scalar):
    pass

class Double(Scalar):
    pass

class Pi(Double):
    def __init__(self):
        pass

    def simplify(self, symtab):
        return math.pi

    def evaluate(self, options):
        return math.pi

    def __repr__(self):
        return "pi"

class Complex(Number):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def isConst(self, symtab=None):
        if isinstance(self.real, numbers.Real) and isinstance(self.real, numbers.Real):
            return True
        return self.real.isConst(symtab) and self.imaginary.isConst(symtab)

    def simplify(self, symtab):
        self.real = self.real.simplify(symtab)
        self.imaginary = self.imaginary.simplify(symtab)

        if self.isConst(symtab):
            return self.value()

        return self

    def value(self):
        return complex(self.real, self.imaginary)

    def __repr__(self):
        return "Complex(%s, %s)" % (self.real, self.imaginary)

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

    def simplify(self, symtab):
        self.number = self.number.simplify(symtab)
        if self.number.isConst(symtab):
            return calc(number)
        return self

    def evaluate(self, options):
        raise NotImplementedError

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.number)

class w(Function):
    def __init__(self, n, k=None):
        self.n = n
        self.k = k

    def simplify(self, symtab):
        raise NotImplementedError #TODO

    def evaluate(self, options):
        raise NotImplementedError #TODO

    def __repr__(self):
        if self.k is None:
            return "w(%s)" % (self.n)
        return "w(%s %s)" % (self.n, self.k)

##### Operators #####
class Operator(Node):
    """func is one of 'add', 'sub', 'mul', 'div' and calls
    the respective __func__ python functions"""
    def __init__(self, left, func, right=None):
        self.left = left
        self.right = right
        self.func = func

    def isConst(self, symtab=None):
        if isinstance(self.left, numbers.Number) and (self.right is None or isinstance(self.right, numbers.Number)):
            return True

        if hasattr(self.left, 'isConst') and (self.right is None or hasattr(self.right, 'isConst')):
            return self.left.isConst(symtab) and (self.right is None or self.right.isConst(symtab))
        return False

    def calc(self):
        """This performs the actual operation. If __%s__ returns
        NotImplemented, then we have to try __r%s__"""
        #print type(self.left), self.func, type(self.right)
        val = NotImplemented

        f = '__%s__' % (self.func.lower())
        fl = None
        if hasattr(self.left, f):
            fl = getattr(self.left, f)
            if self.right is None:
                val = fl()
            else:
                val = fl(self.right)
            if val is not NotImplemented:
                return val

        rf ='__r%s__' % (self.func.lower())
        rfr = None
        if hasattr(self.right, rf):
            rfr = getattr(self.right, rf)
            val = rfr(self.left)
            if val is not NotImplemented:
                return val

        t = self.left.__coerce__(self.right)
        if t is not NotImplemented and fl:
            val = fl(t[1])
            if val is not NotImplemented:
                return val

        t = self.right.__coerce__(self.left)
        if t is not NotImplemented and rfr:
            val = rfr(t[1])
            if val is not NotImplemented:
                return val
        return NotImplemented

    def simplify(self, symtab):
        self.left = self.left.simplify(symtab)
        if self.right is not None:
            self.right = self.right.simplify(symtab)

        if self.isConst(symtab):
            return self.calc()

        return self

    def __repr__(self):
        return "%s(%s, %s)" % (self.func, self.left, self.right)

##### 1.1 Predefined Matrix Constructors ######
class MatrixRow(Formula):
    def __init__(self, values):
        self.n = len(values)
        self.values = values

    def prepend(self, a):
        self.values.insert(0, a)
        self.n += 1

    def simplify(self, symtab):
        self.values = [ i.simplify(symtab) for i in self.values ]
        return self

    def size(self):
        return len(self)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "MatrixRow(%s)" % (self.values)

class Matrix(Formula):
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

    def simplify(self, symtab):
        self.rows = [ i.simplify(symtab) for i in self.rows ]
        return self

    def size(self):
        return (m, n)

    def __repr__(self):
        return "Matrix(%s)" % (self.rows)

class SparseElement(Formula):
    def __init__(self, i, j, a):
        self.i = i
        self.j = j
        self.a = a

    #TODO should eliminate sparseelement if possible
    def simplify(self, symtab):
        self.i = self.i.simplify(symtab)
        self.j = self.j.simplify(symtab)
        self.a = self.a.simplify(symtab)
        return self

    def __repr__(self):
        return "SparesElement(%s %s %s)" % (self.i, self.j, self.a)

class Sparse(Formula):
    def __init__(self, values):
        self.m = 0
        self.n = 0
        self.values = values
        for v in values:
            self.m = v.i if v.i > self.m else self.m
            self.n = v.j if v.j > self.n else self.n

    def simplify(self, symtab):
        self.values = [ i.simplify(symtab) for i in self.values ]
        return self

    def simplify(self, symtab):
        self.values = [ i.simplify(symtab) for i in self.values ]
        return self

    def size(self):
        return (m, n)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "Sparse(%s)" % (self.values)

# class Index(Node):
#     def __init__(self, start, stride, stop):
#         self.start = start
#         self.stride = stride
#         self.stop = stop

#     #TODO should eliminate Index if possible
#     def simplify(self, symtab):
#         node, optStart = self.start.simplify(symtab)
#         if optStart:
#             self.start = node

#         node, optStride = self.stride.simplify(symtab)
#         if optStride:
#             self.stride = node

#         node, optStop = self.stop.simplify(symtab)
#         if optStop:
#             self.stop = node
#         return None, False

#     def __repr__(self):
#         return "Index(%s, %s, %s)" % (self.start, self.stride, self.stop)

##### 1.2 Predefined Parametrized Matrices ######
# class T(Formula):
#     def __init__(self, mn, n, index=None):
#         self.mn = mn
#         self.n = n
#         self.index = index

#     def simplify(self, symtab):
#         node, optMN = self.mn.simplify(symtab)
#         if optMN:
#             self.mn = node
#         node, optN = self.n.simplify(symtab)
#         if optN:
#             self.n = node
#         return None, False

#     def __repr__(self):
#         return "(T %s %s %s)" % (self.mn, self.n, self.index)

##### 1.3 Predefined Matrix Operations ######

class Scale(Formula):
    def __init__(self, a, A):
        self.a = a
        self.A = A

    def simplify(self, symtab):
        self.a = self.a.simplify(symtab)
        self.A = self.A.simplify(symtab)
        return self

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
        return symtab.isConst(self.symbol)

    def simplify(self, symtab):
        self.value = self.value.simplify(symtab)
        symtab[self.symbol] = self.value
        return None

    def __repr__(self):
        return "Define(%s, %s)" % (self.symbol, self.value)

class Undefine(Assignment):
    def __init__(self, symbol, value):
        self.symbol = symbol

    def simplify(self, symtab):
        del symtab[self.symbol]
        return None

    def __repr__(self):
        return "Undefine(%s)" % (self.symbol)

class Symbol(Node):
    def __init__(self, symbol):
        self.symbol = symbol

    def isConst(self,symtab=None):
        return symtab.isConst(self.symbol)

    def simplify(self, symtab):
        if self.isConst(symtab):
            return symtab[self.symbol]
        return self

    def __repr__(self):
        return "Symbol(%s)" % (self.symbol)

##### 2.2 Directive ######
class Directive(Node):
    def __init__(self, value=None):
        self.value = value

    def simplify(self, symtab):
        return self

    def evaluate(self, options):
        options[self.__class__.__name__.lower()] = self.value

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.value)

##### 2.3 Comments ######
class Comment(Node):
    def __init__(self, txt):
        self.txt = txt

    def simplify(self, symtab):
        return self

    def evaluate(self, options):
        return self.txt

    def __repr__(self):
        return "Comment(\"%s\")" % (self.txt)

class Intrinsic(Node):
    def simplify(self, symtab):
        return self

class W(Intrinsic):
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def __repr__(self):
        return "W(%s %s)" % (self.n, self.k)

class WR(Intrinsic):
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def __repr__(self):
        return "WR(%s %s)" % (self.n, self.k)

class WI(Intrinsic):
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def __repr__(self):
        return "WI(%s %s)" % (self.n, self.k)

class TW(Intrinsic):
    def __init__(self, mn, n, k):
        self.mn = mn
        self.n = n
        self.k = k

    def __repr__(self):
        return "TW(%s %s %s)" % (self.mn, self.n, self.k)

class TWR(Intrinsic):
    def __init__(self, mn, n, k):
        self.mn = mn
        self.n = n
        self.k = k

    def __repr__(self):
        return "TWR(%s %s %s)" % (self.mn, self.n, self.k)

class TWI(Intrinsic):
    def __init__(self, mn, n, k):
        self.mn = mn
        self.n = n
        self.k = k

    def __repr__(self):
        return "TWI(%s %s %s)" % (self.mn, self.n, self.k)

class C(Intrinsic):
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def __repr__(self):
        return "C(%s %s)" % (self.n, self.k)

class S(Intrinsic):
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def __repr__(self):
        return "S(%s %s)" % (self.n, self.k)

##### A.1 Errors #####
class ConstantError(ValueError):
    def __init__(self, msg):
        self.msg = "'%s' is not a constant" % (msg)
