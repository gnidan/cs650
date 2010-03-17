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
import types
import symbols
from options import Options
from icodelist import ICodeList

class Node(object):
    def __init__(self):
        raise NotImplementedError

    def simplify(self, symtab):
        '''Performs simplification of the AST. Propagates defines, folds constants, etc.'''
        print "OPTIMIZING: %s" % (self.__class__.__name__)
        return self

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
    def __init__(self, symbol, args, stride=None):
        if(len(args) == 0):
            raise IndexError

        self.stride = stride
        self.list = args
        self.symbol = symbol
        self.ny = 0
        self.nx = 0

        self.a  = None

        self.x = None
        self.y = None
 
    def definition(self, symtab, options):
        if options.unroll:
            pass #TODO gen_code
        else:
            return symbols.Formula(self.value)
 
    def evaluate(self, symtab, options):
        try:
          declaration = symtab[self.symbol]
        except KeyError:
          raise NameError("%s not declared" % self.symbol)

        icodes, records = symtab[self]
        print "starting simplify"
        icodes = icodes.simplify(records)
        print "finishing simplify"
        icodes = ICodeList(icodes)
        return icodes

    def simplify(self, symtab):
        self.list = [ i.simplify(symtab) for i in self.list ]
        self.list = [ i for i in self.list if i ]
        try:
          declaration = symtab[self.symbol]
        except KeyError:
          raise NameError("%s not declared" % self.symbol)
        self.ny, self.nx = declaration.sizes_for(self)
        return self

    def pvars(self):
        vars = {}
        nx = self.nx
        ny = self.ny
        vars["nx"] = symbols.VarR(val=nx)
        vars["ny"] = symbols.VarR(val=ny)
        vars["nx_1"] = symbols.VarR(val=nx-1)
        vars["ny_1"] = symbols.VarR(val=ny-1)
        return vars

    def __len__(self):
        return len(self.list)
 
    def __repr__(self):
        r = str(self.symbol)
        r += "("
        for i in range(len(self.list)):
          arg = self.list[i]
          if( i == 0 ):
            r += str(arg)
          else:
            r += ", "
            r += str(arg)

        if self.stride:
          r += " @ %s:%s:%s" % self.stride
 
        r += ")"
        
        return r

class Program(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def evaluate(self, symtab, options):
        return self.stmts.evaluate(symtab, options)

    def simplify(self, symtab):
        self.stmts = self.stmts.simplify(symtab)
        return self

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

    def __repr__(self):
        return "%s" % (self.val)

class Integer(int, Scalar):
    pass

class Double(Scalar):
    pass

class Pi(Double):
    def __init__(self):
        pass

    def simplify(self, symtab):
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

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.number)

class w(Function):
    def __init__(self, n, k=None):
        self.n = n
        self.k = k

    def simplify(self, symtab):
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

class Symbol(str, Node):
    def __init__(self, symbol):
        self.symbol = symbol

    def isConst(self,symtab=None):
        return symtab.isConst(self.symbol)

    def simplify(self, symtab):
        if self.isConst(symtab):
            return symtab[self.symbol]
        raise NameError("%s not assigned constant value. Cannot simplify" % 
            self)
        return self

    def __repr__(self):
        return "Symbol(%s)" % (self.symbol)

    def __str__(self):
        return self.symbol

##### 2.2 Directive ######
class Directive(Node):
    def __init__(self, value=None):
        self.value = value

    def simplify(self, symtab):
        return self

    def evaluate(self, symtab, options):
        options[self.__class__.__name__.lower()] = self.value
        return []

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.value)

##### 2.3 Comments ######
class Comment(Node):
    def __init__(self, txt):
        self.txt = txt

    def simplify(self, symtab):
        return self

    def evaluate(self, symtab, options):
        return ICodeList([self])

    def __repr__(self):
        return "Comment(\"%s\")" % (self.txt)

class Intrinsic(Node):
    #REFACTOR
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

##### 3.1 Symbol Declaration #####
class Primitive(Assignment):
    def __init__(self, symbol, shape):
        self.symbol = symbol
        self.shape = shape

    def simplify(self, symtab):
        symtab[self.symbol] = symbols.Primitive(self.shape)
        return None
 
class Operation(Assignment):
    def __init__(self, symbol, size_rule):
        self.symbol = symbol
        self.size_rule = size_rule

    def simplify(self, symtab):
        symtab[self.symbol] = symbols.Operation(self.size_rule)
        return None
 
class Direct(Assignment):
    def __init__(self, symbol, size_rule):
        self.symbol = symbol
        self.size_rule = size_rule

    def simplify(self, symtab):
        symtab[self.symbol] = symbols.Direct(self.size_rule)
        return None
 
##### 3.2 Templates ######
class Template(Assignment):
    def __init__(self, pattern, icode_list, condition=None):
        self.pattern = pattern
        self.condition = condition
        self.icode_list = icode_list
 
    def isConst(self, symbtab=None):
        return False

    def simplify(self, symtab):
        if self.pattern.symbol not in symtab:
            raise NameError("%s not declared before being used" % 
                self.pattern.symbol)
        symtab[self.pattern.symbol].addTemplate(self)
        return None

    def __repr__(self):
        return "Template(%s, %s)" % (self.pattern, self.icode_list)
 
class Condition(Node):
  pass
 
class Wildcard(Symbol):
  pass

##### A.1 Errors #####
class ConstantError(ValueError):
    def __init__(self, val):
        self.msg = "'%s' is not a constant" % (val)
