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

    def optimize(self, symtab, options):
        '''Performs early optimizations on the AST such as Constant Folding'''
        print self.__class__.__name__
        raise NotImplementedError

    def evaluate(self, symtab, options):
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
    def definition(self, symtab, options):
        if options.unroll:
            pass #TODO gen_code
        else:
            return symbols.Formula(self.value)

    def evaluate(self, symtab, options):
        print "Must implement Formula evaluate"


class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def evaluate(self, symtab, options):
        self.stmts.evaluate(symtab, options)

    def optimize(self, symtab, options):
        self.stmts.optimize(symtab, options)

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

    def evaluate(self, symtab, options):
        return [s.evaluate(symtab, options) for s in self.stmts]

    def optimize(self, symtab, options):
        #List comprehension wasn't pretty. But i don't like xrange either :-(
        for i in xrange(len(self)):
            node, opt = self.stmts[i].optimize(symtab, options)
            if opt:
                self.stmts[i] = node
        return None, False

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

    def optimize(self, symtab, options):
        return self.value(), True

    def evaluate(self, symtab, options):
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

    def optimize(self, symtab, options):
        return math.pi, True

    def evaluate(self, symtab, options):
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

    def optimize(self, symtab, options):
        node, optR = self.real.optimize(symtab, options)
        if optR:
            self.real = node

        node, optI = self.imaginary.optimize(symtab, options)
        if optI:
            self.imaginary = node

        if optR and optI:
            return self.value(), True
        return None, False

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

    def optimize(self, symtab, options):
        node, opt = self.number.optimize(symtab, options)
        if opt:
            self.number = node
            return calc(number), True
        return None, False

    def evaluate(self, symtab, options):
        raise NotImplementedError

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

    def optimize(self, symtab, options):
        raise NotImplementedError #TODO

    def evaluate(self, symtab, options):
        raise NotImplementedError #TODO

    def __repr__(self):
        if self.k is None:
            return "w(%s)" % (self.n)
        return "w(%s %s)" % (self.n, self.k)

##### Operators #####
class Operator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def calc(self):
        '''This performs the actual operation'''
        raise NotImplementedError

    def isConst(self):
        return False

    def optimize(self, symtab, options):
        node, optL = self.left.optimize(symtab, options)
        if optL:
            self.left = node

        node, optR = self.right.optimize(symtab, options)
        if optR:
            self.right = node

        if optL and optR:
            return self.calc(), True

        return None, False

    def evaluate(self, symtab, options):
        raise NotImplementedError #TODO

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.left, self.right)

class Add(Operator):
    def calc(self):
        return self.left + self.right

class Sub(Operator):
    def calc(self):
        return self.left - self.right

class Mul(Operator):
    def calc(self):
        return self.left * self.right

class Div(Operator):
    def calc(self):
        return self.left / self.right

class Mod(Operator):
    def calc(self):
        return self.left % self.right

class Neg(Operator):
    def __init__(self, val):
        self.val = val

    def isConst(self, symtab=None):
        return self.val.isConst(symtab)

    def optimize(self, symtab, options):
        node, opt = self.val.optimize(symtab, options)
        if opt:
            self.val = node
            return (-node, True)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.val)

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

    def optimize(self, symtab, options):
        for i in xrange(self.n):
            node, opt = self.values[i].optimize(symtab, options)
            if opt:
                self.values[i] = node
        return None, False

    def size(self):
        return len(self)

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

    def optimize(self, symtab, options):
        for i in xrange(self.m):
            node, opt = self.rows[i].optimize(symtab, options)
            if opt:
                self.rows[i] = node
        return None, False

    def size(self):
        return (m, n)

    def __repr__(self):
        return "Matrix(%s)" % (self.rows)

class Diagonal(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values

    def optimize(self, symtab, options):
        for i in xrange(self.n):
            node, opt = self.values[i].optimize(symtab, options)
            if opt:
                self.values[i] = node
        return None, False

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "Diagonal(%s)" % (self.values)

class Permutation(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values


    def optimize(self, symtab, options):
        for i in xrange(self.n):
            node, opt = self.values[i].optimize(symtab, options)
            if opt:
                self.values[i] = node
        return None, False

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "Permutation(%s)" % (self.values)

class RPermutation(Constructor):
    def __init__(self, values):
        self.n = len(values)
        self.values = values


    def optimize(self, symtab, options):
        for i in xrange(self.n):
            node, opt = self.values[i].optimize(symtab, options)
            if opt:
                self.values[i] = node
        return None, False

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "RPermutation(%s)" % (self.values)

class SparseElement(Constructor):
    def __init__(self, i, j, a):
        self.i = i
        self.j = j
        self.a = a

    #TODO should eliminate sparseelement if possible
    def optimize(self, symtab, options):
        node, optI = self.i.optimize(symtab, options)
        if optI:
            self.i = node

        node, optJ = self.j.optimize(symtab, options)
        if optI:
            self.j = node

        node, optA = self.a.optimize(symtab, options)
        if optI:
            self.a = node

        return None, False

    def __repr__(self):
        return "SparesElement(%s %s %s)" % (self.i, self.j, self.a)

class Sparse(Constructor):
    def __init__(self, values):
        self.m = 0
        self.n = 0
        self.values = values
        for v in values:
            self.m = v.i if v.i > self.m else self.m
            self.n = v.j if v.j > self.n else self.n

    def optimize(self, symtab, options):
        for i in xrange(len(self)):
            node, opt = self.values[i].optimize(symtab, options)
            if opt:
                self.values[i] = node
        return None, False

    def size(self):
        return (m, n)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return "Sparse(%s)" % (self.values)

class Index(Node):
    def __init__(self, start, stride, stop):
        self.start = start
        self.stride = stride
        self.stop = stop

    #TODO should eliminate Index if possible
    def optimize(self, symtab, options):
        node, optStart = self.start.optimize(symtab, options)
        if optStart:
            self.start = node

        node, optStride = self.stride.optimize(symtab, options)
        if optStride:
            self.stride = node

        node, optStop = self.stop.optimize(symtab, options)
        if optStop:
            self.stop = node
        return None, False

    def __repr__(self):
        return "Index(%s, %s, %s)" % (self.start, self.stride, self.stop)

##### 1.2 Predefined Parametrized Matrices ######
class ParametrizedMatrix(Formula):
    pass

class F(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def optimize(self, symtab, options):
        node, optN = self.n.optimize(symtab, options)
        if optN:
            self.n = node
        return None, False

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

    def optimize(self, symtab, options):
        node, optM = self.m.optimize(symtab, options)
        if optM:
            self.m = node
        node, optN = self.n.optimize(symtab, options)
        if optN:
            self.n = node
        return None, False

    def __repr__(self):
        return "(I %s %s)" % (self.m, self.n)

class J(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def optimize(self, symtab, options):
        node, optN = self.n.optimize(symtab, options)
        if optN:
            self.n = node
        return None, False

    def __repr__(self):
        return "(J %s)" % (self.n)

class O(ParametrizedMatrix):
    def __init__(self, n):
        self.n = n

    def optimize(self, symtab, options):
        node, optN = self.n.optimize(symtab, options)
        if optN:
            self.n = node
        return None, False

    def __repr__(self):
        return "(O %s)" % (self.n)

class T(ParametrizedMatrix):
    def __init__(self, mn, n, index=None):
        self.mn = mn
        self.n = n
        self.index = index

    def optimize(self, symtab, options):
        node, optMN = self.mn.optimize(symtab, options)
        if optMN:
            self.mn = node
        node, optN = self.n.optimize(symtab, options)
        if optN:
            self.n = node
        return None, False

    def __repr__(self):
        return "(T %s %s %s)" % (self.mn, self.n, self.index)

class L(ParametrizedMatrix):
    def __init__(self, mn, n):
        self.mn = mn
        self.n = n

    def optimize(self, symtab, options):
        node, optMN = self.mn.optimize(symtab, options)
        if optMN:
            self.mn = node
        node, optN = self.n.optimize(symtab, options)
        if optN:
            self.n = node
        return None, False

    def __repr__(self):
        return "(L %s %s)" % (self.mn, self.n)

##### 1.3 Predefined Matrix Operations ######
class Operation(Formula):
    pass

class Compose(Operation):
    def __init__(self, formulas):
        self.formulas = formulas


    def optimize(self, symtab, options):
        for i in xrange(len(self.formulas)):
            node, opt = self.formulas[i].optimize(symtab, options)
            if opt:
                self.formulas[i] = node
        return None, False

    def __repr__(self):
        return "Compose(%s)" % (self.formulas)

class Tensor(Operation):
    def __init__(self, formulas):
        self.formulas = formulas

    def optimize(self, symtab, options):
        for i in xrange(len(self.formulas)):
            node, opt = self.formulas[i].optimize(symtab, options)
            if opt:
                self.formulas[i] = node
        return None, False

    def __repr__(self):
        return "Tensor(%s)" % (self.formulas)


class DirectSum(Operation):
    def __init__(self, formulas):
        self.formulas = formulas

    def optimize(self, symtab, options):
        for i in xrange(len(self.formulas)):
            node, opt = self.formulas[i].optimize(symtab, options)
            if opt:
                self.formulas[i] = node
        return None, False

    def __repr__(self):
        return "DirectSum(%s)" % (self.formulas)

class Conjugate(Operation):
    def __init__(self, A, P):
        self.A = A
        self.P = P

    def optimize(self, symtab, options):
        node, optA = self.A.optimize(symtab, options)
        if optA:
            self.A = node
        node, optP = self.P.optimize(symtab, options)
        if optP:
            self.P = node
        return None, False

    def __repr__(self):
        return "Conjugate(%s %s)" % (self.A, self.P)

class Scale(Operation):
    def __init__(self, a, A):
        self.a = a
        self.A = A

    def optimize(self, symtab, options):
        node, opta = self.a.optimize(symtab, options)
        if opta:
            self.a = node
        node, optA = self.A.optimize(symtab, options)
        if optA:
            self.A = node
        return None, False

    def __repr__(self):
        return "Scale(%s %s)" % (self.a, self.A)

##### 2.1 Assignment ######
class Assignment(Node):
    pass

class Template(Assignment):
    def __init__(self, pattern, icode_list, condition=None):
        self.pattern = pattern
        self.condition = condition
        self.icode_list = icode_list

    def isConst(self, symbtab=None):
        return False

    def evaluate(self, symtab, options):
        # buhh gotta think about this one :) TODO
        symtab[self.pattern.symbol] = (
            self.pattern.evaluate(symtab, options), 
            self.icode_list.evaluate(symtab, options
              )

class Define(Assignment):
    def __init__(self, symbol, value, const=False):
        self.symbol = symbol
        self.value = value

    def isConst(self,symtab=None):
        return symtab.isConst(self.symbol)

    def optimize(self, symtab, options):
        node, opt = self.value.optimize(symtab, options)
        if opt:
            symtab[self.symbol] = node
            self.value = node
        else:
            symtab[self.symbol] = self.value
        return None, False

    def evaluate(self, symtab, options):
        #print "Symbol: %s" % self.symbol
        #print "Value: %s" % self.value
        symtab[self.symbol] = self.value.evaluate(symtab, options)

    def __repr__(self):
        return "Define(%s, %s)" % (self.symbol, self.value)

class Undefine(Assignment):
    def __init__(self, symbol, value):
        self.symbol = symbol

    def evaluate(self, symtab, options):
        del symtab[self.symbol]

    def __repr__(self):
        return "Undefine(%s)" % (self.symbol)

class Symbol(Node):
    def __init__(self, symbol):
        self.symbol = symbol

    def isConst(self,symtab=None):
        return symtab.isConst(self.symbol)

    def optimize(self, symtab, options):
        if self.isConst(symtab):
            return symtab[self.symbol], True
        return None, False

    def evaluate(self, symtab, options):
        return symtab[self.symbol]

    def __repr__(self):
        return "Symbol(%s)" % (self.symbol)

##### 2.2 Directive ######
class Directive(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symtab, options):
        options[self.__class__.__name__.lower()] = self.value.value()

    #REFACTOR
    def optimize(self, symtab, options):
        return None, False

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

    def evaluate(self, symtab, options):
        return self.value()

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

    def optimize(self, symtab, options):
        return None, False

    def evaluate(self, symtab, options):
        print "%s %s %s" % (options.lang.comment_begin(), self.txt, options.lang.comment_end())

    def __repr__(self):
        return "Comment(\"%s\")" % (self.txt)

class Intrinsic(Node):
    #REFACTOR
    def optimize(self, symtab, options):
        return None, False
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
class ConstantError(ValueError):
    def __init__(self, msg):
        self.msg = "'%s' is not a constant" % (msg)
