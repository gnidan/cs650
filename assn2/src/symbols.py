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

    #TODO: this needs to be fixed!
    def __mul__(self, other):
        if self.val is not None:
            return self.val * other
        return '%s * %s' % (self.num(), other.num())

    def __rmul__(self, other):
        if self.val is not None:
            return other * self.val
        return '%s * %s' % (other.num(), self.num())

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


### VECTORS ###
class Vec(Var):
    var_type = 't'
    def __init__(self, size=None):
        self.size = size
        self.val = None
        self.name = None
        self.out_name = None
        

    def __len__(self):
        return self.size

class IOVec(Vec):
    def __str__(self):
        return self.var_type

class VarIn(IOVec):
    var_type = 'x'

class VarOut(IOVec):
    var_type = 'y'


class IRef:
    var_type = 'i'
    """This is just a reference to a variable $i0, $i1 ... """
    def __init__(self,ref):
        self.ref = ref

    def __str__(self):
        return "$i%d" % (self.ref)

class Index:
    """This is used to store the index in icode."""
    def __init__(self, vec, exp):
        self.vec = vec
        self.exp = exp

    def idx(self, stack=None):
        #Calculate our accumulator and the multiplies
        accum = self.exp[0]
        idxs = [ e * i for (e, i) in zip(self.exp[1:], stack) ]

        #The multiplies can be either str or int. sum them up or concatenate
        accum += sum([ i for i in idxs if isinstance(i, int) ])
        strs = [ i for i in idxs if isinstance(i, str) ]
        if len(strs):
            s = '+'.join(strs)
            if accum > 0:
                s += "+%d" % (accum)
            if accum < 0:
                s += "-%d" % (-accum)
            return (self.vec, s)
        return (self.vec, accum)

    def num(self):
        return self

    def __str__(self):
        return "Index(%s, %s)" % (self.vec, self.exp)
