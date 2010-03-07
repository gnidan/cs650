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

class Node(object):
    def __init__(self):
        raise NotImplementedError

    def optimize(self, symtab, options):
        '''Performs early optimizations on the AST such as Constant Folding'''
        print "OPTIMIZING: %s" % (self.__class__.__name__)
        return None, False

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
    def __init__(self, *args):
        if(len(args) == 0):
            raise IndexError
 
        self.list = args
        self.symbol = args[0]
 
    def definition(self, symtab, options):
        if options.unroll:
            pass #TODO gen_code
        else:
            return symbols.Formula(self.value)
 
    def evaluate(self, symtab, options):
        print "Must implement Formula evaluate"
 
    def __repr__(self):
        r = ""
        for i in range(len(self.list)):
          arg = self.list[i]
          if( i == 0 ):
            r += arg.symbol
            r += "("
          elif( i == 1 ):
            r += repr(arg)
          else:
            r += ", "
            r += repr(arg)
 
        r += ")"
        
        return r

class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def evaluate(self, symtab, options):
        return self.stmts.evaluate(symtab, options)

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
    """func is one of 'add', 'sub', 'mul', 'div' and calls
    the respective __func__ python functions"""
    def __init__(self, left, func, right=None):
        self.left = left
        self.right = right
        self.func = func

    def isConst(self):
        if hasattr(self.left, 'isConst') and (self.right is None or hasattr(self.right, 'isConst')):
            return self.left.isConst() and (self.right is None or self.right.isConst())
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

    def optimize(self, symtab, options):
        node, optL = self.left.optimize(symtab, options)
        if optL:
            self.left = node

        optR = True
        if self.right:
            node, optR = self.right.optimize(symtab, options)
            if optR:
                self.right = node

        if optL and optR:
            return self.calc(), True
        return None, False

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

    def optimize(self, symtab, options):
        for i in xrange(self.n):
            node, opt = self.values[i].optimize(symtab, options)
            if opt:
                self.values[i] = node
        return self.values, True

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

class SparseElement(Formula):
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

class Sparse(Formula):
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
class T(Formula):
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

##### 1.3 Predefined Matrix Operations ######

class Scale(Formula):
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
        #TODO this is hackish. is there a better way?
        if not isinstance(self.value, numbers.Number):
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
    def __init__(self, value=None):
        self.value = value

    #TODO eliminate
    def optimize(self, symtab, options):
        return None, False

    def evaluate(self, symtab, options):
        options[self.__class__.__name__.lower()] = self.value
        #TODO how do we correctly do subnames and other directives? ugh.
        #return self

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.value)

##### 2.3 Comments ######
class Comment(Node):
    def __init__(self, txt):
        self.txt = txt

    def optimize(self, symtab, options):
        return None, False

    def evaluate(self, symtab, options):
        #TODO fix
        return self.txt
#print "%s %s %s" % (options.lang.comment_begin(), self.txt, options.lang.comment_end())

    def __repr__(self):
        return "Comment(\"%s\")" % (self.txt)

class Intrinsic(Node):
    #REFACTOR
    def optimize(self, symtab, options):
        return None, False
    pass

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

##### 3.1 Symbol Declaration #####
class Primitive(Assignment):
    def __init__(self, symbol, shape):
        self.symbol = symbol
        self.shape = shape
 
class Operation(Assignment):
    def __init__(self, symbol, size_rule):
        self.symbol = symbol
        self.size_rule = size_rule
 
class Direct(Assignment):
    def __init__(self, symbol, size_rule):
        self.symbol = symbol
        self.size_rule = size_rule
 
##### 3.2 Templates ######
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
            self.icode_list.evaluate(symtab, options)
              )
 
    def __repr__(self):
        return "Template(%s, %s)" % (self.pattern, self.icode_list)
 
class Condition(Node):
  pass
 
class Pattern(Symbol):
    def __init__(self, symbol, formulas):
      self.symbol = symbol
      self.formulas = formulas
 
class Wildcard(Symbol):
  pass

##### A.1 Errors #####
class ConstantError(ValueError):
    def __init__(self, msg):
        self.msg = "'%s' is not a constant" % (msg)
