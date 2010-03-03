#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

symbols.py Contains all of the variable types referenced at various stages of ICode.
"""

import numbers

class NextVarSet:
    def __init__(self):
        #print 'NextVarSet created'
        self.vars = {}

    def __getitem__(self, key):
        if key not in self.vars:
            self.vars[key] = 0
        i = self.vars[key]
        self.vars[key] += 1
        return "%s%d" % (key, i)
        #return i

class Var:
    var_type = 'v'
    next_val = NextVarSet()

    def __init__(self,val=None,name=None):
        self.val = None
        self.name = None
        self.out_name = None

    def num(self):
        if self.val is not None:
            if hasattr(self.val, 'num'):
                return getattr(self.val, 'num')()
            return self.val
        return self

    def __str__(self):
        if self.val is not None:
            if hasattr(self.val, 'num'):
                return str(getattr(self.val, 'num')())
            #return str(self.val)
        if not self.name:
            self.name = "%s" % (self.__class__.next_val[self.__class__.var_type])
        return '$%s' % (self.name)

    def __repr__(self):
        return str(self)

#TODO we should construct these dynamically?
class VarR(Var):
    var_type = 'r'

class VarF(Var):
    var_type = 'f'

class DoVar(Var):
    """This is used in Do Loops to indicate the current loop value"""
    def __init__(self,inst,n,val=0):
        self.inst = inst #The instruction this variable is associated with.
        self.n = n # The value that this variable goes up to
        self.val = val #The present value during a particular unrolling step

    def __str__(self):
        return "DoVar(val=%d, n=%d, inst=%d)" % (self.val, self.n, self.inst)

class IRef(Var):
    var_type = 'i'
    """This is just a reference to a variable $i0, $i1 ... """
    def __init__(self,val):
        self.val = val

    def __str__(self):
        return "$i%d" % (self.val)

class Vec(Var):
    var_type = 't'

class IOVec(Vec):
    def __str__(self):
        return self.var_type

class VarIn(IOVec):
    var_type = 'x'

class VarOut(IOVec):
    var_type = 'y'




class Index:
    """This is used to store the index in icode."""
    def __init__(self, vec, exp):
        self.vec = vec
        self.exp = exp

    def idx(self, stack=None):
        accum = self.exp[0]
        idxs = []
        e = self.exp[1:]
        for e,i in zip(self.exp[1:], stack):
            if isinstance(i, str):
                idxs.append("%d*%s" % (e, i))
            elif isinstance(i.val, numbers.Integral):
                accum += e * i.val
            elif isinstance(i, Var):
                idxs.append("%d*%s" % (e, i.val))
            else:
                raise TypeError
        if not idxs:
            return (self.vec, accum)
        idxs.append(str(accum))
        return (self.vec, '+'.join(idxs))

    def num(self):
        return self

    def __str__(self):
        return "Index(%s, %s)" % (self.vec, self.exp)
