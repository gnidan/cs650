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
from flags import Flags

class Node:
    def __init__(self):
        raise NotImplementedError

    def optimize(self, symtab):
        '''Performs early optimizations on the AST such as Constant Folding'''
        pass

    def evaluate(self, symtab=None, directives=None, lang=C99):
        raise NotImplementedError

    def isConst(self,symtab=None):
        return False

    def __str__(self):
        return repr(self)

    def __repr__(self):
        '''prints the AST in an ATerm like format'''
        raise NotImplementedError

class Formula(Node):
    def definition(self, symtab=None):
        if directives.unroll:
            pass #TODO gen_code
        else:
            return symbols.Formula(self.value)

    def evaluate(self, symtab=None, directives=None, lang=C99):
        print "Must implement Formula"


class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def evaluate(self, symtab=None, directives=None, lang=C99):
        self.stmts.evaluate(symtab=symtab, directives=directives, lang=lang)

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

    def evaluate(self, symtab=None, directives=None, lang=C99):
        for stmt in self.stmts:
            stmt.evaluate(symtab=symtab, directives=directives, lang=lang)

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

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return self.value

class Integer(Scalar):
    pass

class Double(Scalar):
    pass

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
    def evalf(sclr, cmplx, val):
        if isinstance(val, complex):
            return cmplx(val)
        elif isinstance(val, numbers.Real):
            return sclr(val)
        raise ConstantError(val)

class Sin(Function):
    def __init__(self, number):
        self.number = number

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return evalf(math.sin, cmath.sin, self.number.evaluate(symtab=symtab, directives=directives, lang=lang))

    def __repr__(self):
        return "Sin(%s)" % (self.number)

class Cos(Function):
    def __init__(self, number):
        self.number = number

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return evalf(math.cos, cmath.cos, self.number.evaluate(symtab=symtab, directives=directives, lang=lang))

    def __repr__(self):
        return "Cos(%s)" % (self.number)

class Tan(Function):
    def __init__(self, number):
        self.number = number

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return evalf(math.tan, cmath.tan, self.number.evaluate(symtab=symtab, directives=directives, lang=lang))

    def __repr__(self):
        return "Tan(%s)" % (self.number)

class Log(Function):
    def __init__(self, number):
        self.number = number

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return evalf(math.log, cmath.log, self.number.evaluate(symtab=symtab, directives=directives, lang=lang))

    def __repr__(self):
        return "Log(%s)" % (self.number)

class Exp(Function):
    def __init__(self, number):
        self.number = number

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return evalf(math.exp, cmath.exp, self.number.evaluate(symtab=symtab, directives=directives, lang=lang))

    def __repr__(self):
        return "Exp(%s)" % (self.number)

class Sqrt(Function):
    def __init__(self, number):
        self.number = number

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return evalf(math.sqrt, cmath.sqrt, self.number.evaluate(symtab=symtab, directives=directives, lang=lang))

    def __repr__(self):
        return "Sqrt(%s)" % (self.number)

class Pi(Function):
    def __init__(self):
        pass

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return math.pi

    def __repr__(self):
        return "pi"

class w(Function):
    def __init__(self, n, k=None):
        self.n = n
        self.k = k

    def __repr__(self):
        return "w(%s %s)" % (self.n, self.k)

##### Operators #####
class Operator:
    pass

class Add(Operator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Add(%s, %s)" % (self.left, self.right)

class Sub(Operator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Sub(%s, %s)" % (self.left, self.right)

class Mul(Operator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Mul(%s, %s)" % (self.left, self.right)

class Div(Operator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Div(%s, %s)" % (self.left, self.right)


class Mod(Operator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Mod(%s, %s)" % (self.left, self.right)

class Neg(Operator):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Neg(%s)" % (self.value)

##### 1.1 Predefined Matrix Constructors ######
class Constructor(Formula):
    def __init__(self):
        raise NotImplementedError()

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

    def evaluate(self, symtab=None, directives=None, lang=C99):
        #Maybe this should call evaluate?
        print "Symbol: %s" % self.symbol
        print "Value: %s" % self.value
        symtab[self.symbol] = self.value.evaluate(symtab=symtab, directives=directives, lang=lang)

    def __repr__(self):
        return "Define(%s, %s)" % (self.symbol, self.value)

class Undefine(Assignment):
    def __init__(self, symbol, value):
        self.symbol = symbol

    def evaluate(self, symtab=None, directives=None, lang=C99):
        del symtab[self.symbol]

    def __repr__(self):
        return "Undefine(%s)" % (self.symbol)

##### 2.2 Directive ######
class Directive(Node):
    pass

class SubName(Directive):
    def __init__(self, symbol):
        self.symbol = symbol

    def evaluate(self, symtab=None, directives=None, lang=C99):
        directives.subname = self.symbol

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

    def evaluate(self, symtab=None, directives=None, lang=C99):
        directives.optimize = self.flag.evaluate(symtab=symtab, directives=directives, lang=lang)

    def __repr__(self):
        return "Optimize(%s)" % (self.flag)

class Unroll(Directive):
    def __init__(self, flag):
        self.flag = flag

    def evaluate(self, symtab=None, directives=None, lang=C99):
        directives.unroll = self.flag.evaluate(symtab=symtab, directives=directives, lang=lang)

    def __repr__(self):
        return "Unroll(%s)" % (self.flag)

class Verbose(Directive):
    def __init__(self, flag):
        self.flag = flag

    def evaluate(self, symtab=None, directives=None, lang=C99):
        directives.verbose = self.flag.evaluate(symtab=symtab, directives=directives, lang=lang)

    def __repr__(self):
        return "Verbose(%s)" % (self.flag)

class Debug(Directive):
    def __init__(self, flag):
        self.flag = flag

    def evaluate(self, symtab=None, directives=None, lang=C99):
        directives.debug = self.flag.evaluate(symtab=symtab, directives=directives, lang=lang)

    def __repr__(self):
        return "Debug(%s)" % (self.flag)

class Internal(Directive):
    def __init__(self, flag):
        self.flag = flag

    def evaluate(self, symtab=None, directives=None, lang=C99):
        directives.internal = self.flag.evaluate(symtab=symtab, directives=directives, lang=lang)

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

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return True

    def __repr__(self):
        return "on"

class Off(Flag):
    def __init__(self):
        pass

    def evaluate(self, symtab=None, directives=None, lang=C99):
        return False

    def __repr__(self):
        return "off"

##### 2.3 Comments ######
class Comment(Node):
    def __init__(self, txt):
        self.txt = txt

    def evaluate(self, symtab=None, directives=None, lang=C99):
        print "%s %s %s" % (lang.comment_begin(), self.txt, lang.comment_end())

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
