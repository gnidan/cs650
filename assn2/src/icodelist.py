#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

icodelist.py represents the icodelist and optimizations

"""

import numbers

from icode import *
from symbols import *
from intrinsics import *
from symbol_collection import SymbolCollection

import copy

#TODO Need to keep track of a LoopIdx stack
#TODO Need to keep track of a Temp stack

#tolerance = 1e-10

def feq(a,b):
    if abs(a-b)<0.00000001:
        return True
    else:
        return False

def promote_complex(val):
    if isinstance(val, numbers.Complex):
        if val == complex(1,0):
            return int(1)
        if val == complex(-1,0):
            return int(-1)
        if val == complex(0,0):
            return int(0)

        if feq(1, val.real) and feq(0, val.imag):
            return int(1)
        if feq(-1, val.real) and feq(0, val.imag):
            return int(-1)
        if feq(0, val.real) and feq(0, val.imag):
            return int(0)

    return val

def num(val):
    if isinstance(val, numbers.Number):
        return val
    if hasattr(val, 'num'):
        #print 'num = ', getattr(val, 'num')()
        return getattr(val, 'num')()
    return val
    #raise NameError

def isnumeric(val):
    return isinstance(val, numbers.Number)

class ICodeList:
    def __init__(self, icode):
        self.icode = icode

    def varunroll(self, old, stack, varmap, outvar=False):
        #print 'varunroll', old
        if isnumeric(old):
            return old
        elif isinstance(old, Intrinsic):
            #n, k, mn
            #TODO this is ugly
            new = copy.copy(old)
            if hasattr(new, 'n'):
                v = self.varunroll(new.n, stack, varmap, False)
                #print 'n = ', v
                new.n = v
            if hasattr(new, 'k'):
                v = self.varunroll(new.k, stack, varmap, False)
                #print 'k = ', v
                new.k = v
            if hasattr(new, 'mn'):
                new.mn = self.varunroll(new.mn, stack, varmap, False)
            return new
        elif isinstance(old, Vec):
            return old
        elif isinstance(old, Index):
            if isinstance(old.vec, Vec):
                if isinstance(old.exp, list):
                    return old.idx(stack)
            return old
        elif isinstance(old, DoVar):
            raise TypeError
        elif isinstance(old, IRef):
            return stack[old.val].val
        #We want to do SSA. If we are an output variable, create
        #a new map. Otherwise we want to use our old value.
        elif outvar:
            varmap[old] = old.__class__(old.val, old.name)
            return varmap[old]
        elif old in varmap:
            return varmap[old]
        else:
            return old

    def unroll(self):
        Var.next_val = NextVarSet()
        unrolled = []
        stack = []
        varmap = {}
        i = 0
        while i < len(self.icode):
            inst = self.icode[i]

            #LOOPS
            if isinstance(inst, Do):
                stack.insert(0, DoVar(i,inst.src1))
            elif isinstance(inst, End):
                stack[0].val += 1
                #if < then we still have to loop, otherwise move on
                if stack[0].val < stack[0].n:
                    i = stack[0].inst
                else:
                    stack = stack[1:]

            elif isinstance(inst, Call):
                #TODO
                pass

            elif isinstance(inst, DefTmp):
                unrolled.append(DefTmp(inst.src1))
                #TODO

            #OPERATIONS
            elif isinstance(inst, OpICode):
                src1 = self.varunroll(inst.src1, stack, varmap, False)
                src2 = self.varunroll(inst.src2, stack, varmap, False)
                dest = self.varunroll(inst.dest, stack, varmap, True)
                unrolled.append(inst.__class__(src1, src2, dest))
            elif isinstance(inst, Copy):
                src1 = self.varunroll(inst.src1, stack, varmap, False)
                dest = self.varunroll(inst.dest, stack, varmap, True)
                unrolled.append(Copy(src1, dest))
            i+=1

        self.icode = unrolled

    def constprop(self):
        Var.next_val = NextVarSet()
        i = 0
        while i < len(self.icode):
            inst = self.icode[i]

            if isinstance(inst, OpICode):
                #print inst
                # print 'src1', inst.src1, num(inst.src1)
                # if isinstance(inst.src1, Var):
                #     print 'val = ', inst.src1.val
                # print 'src2', inst.src2, num(inst.src2)
                # if isinstance(inst.src2, Var):
                #     print 'val = ', inst.src2.val
                src1 = num(inst.src1)
                src2 = num(inst.src2)

                if isinstance(src1, numbers.Complex):
                    src1 = promote_complex(src1)
                if isinstance(src2, numbers.Complex):
                    src2 = promote_complex(src2)

                if src1:
                    inst.src1 = src1
                if src2:
                    inst.src2 = src2

                if isinstance(inst, Add):
                    if isnumeric(src1) and isnumeric(src2):
                        inst.dest.val = src1 + src2
                        #print 'add', inst.dest,'<-',inst.dest.val
                        self.icode[i] = None
                    elif src1 == 0:
                        inst.dest.val = src2
                        self.icode[i] = None
                    elif src2 == 0:
                        inst.dest.val = src1
                        self.icode[i] = None

                elif isinstance(inst, Sub):
                    if isnumeric(src1) and isnumeric(src2):
                        inst.dest.val = src1 - src2
                        #print 'sub', inst.dest,'<-',inst.dest.val
                        self.icode[i] = None
                    elif src2 == 0:
                        inst.dest.val = src1
                        self.icode[i] = None

                elif isinstance(inst, Mul):
                    if isnumeric(src1) and isnumeric(src2):
                        inst.dest.val = src1 * src2
                        #print 'mul', inst.dest,'<-',inst.dest.val
                        self.icode[i] = None
                    elif src1 == 1:
                        inst.dest.val = src2
                        self.icode[i] = None
                    # elif src1 == -1:
                    #     inst.dest.val = -src2
                    #     self.icode[i] = None
                    elif src2 == 1:
                        inst.dest.val = src1
                        self.icode[i] = None
                    # elif src2 == -1:
                    #     inst.dest.val = -src1
                    #     self.icode[i] = None
                    elif src1 == 0 or src2 == 0:
                        inst.dest.val = 0
                        self.icode[i] = None

                elif isinstance(inst, Div):
                    if isnumeric(src1) and isnumeric(src2):
                        inst.dest.val = src1 / src2
                        #print 'div', inst.dest,'<-',inst.dest.val
                        self.icode[i] = None
                    elif src1 == 0:
                        inst.dest.val = 0
                        self.icode[i] = None
                    elif src2 == 1:
                        inst.dest.val = src1
                        self.icode[i] = None
                    # elif src2 == -1:
                    #     inst.dest.val = -src1
                    #     self.icode[i] = None
                    elif src2 == 0:
                        raise ZeroDivisionError

                elif isinstance(inst, Mod):
                    if isnumeric(src1) and isnumeric(src2):
                        inst.dest.val = src1 % src2
                        self.icode[i] = None
                    elif src1 == 0:
                        inst.dest.val = 0
                        self.icode[i] = None
                    elif src2 == 1:
                        inst.dest.val = 0
                        self.icode[i] = None
                    elif src2 == 0:
                        raise ZeroDivisionError

            elif isinstance(inst, Copy):
                src1 = num(inst.src1)
                if src1 is not None:
                    if not isinstance(src1, tuple):
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = src1.val
                            self.icode[i] = None

            i+=1

        #Remove any None placeholders
        self.icode = [i for i in self.icode if i]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join([str(i) for i in self.icode])

    def count(self):
        add = 0
        sub = 0
        mul = 0
        div = 0
        mod = 0
        cpy = 0
        for i in self.icode:
            if isinstance(i, Add):
                add += 1
            if isinstance(i, Sub):
                sub += 1
            if isinstance(i, Mul):
                mul += 1
            if isinstance(i, Div):
                div += 1
            if isinstance(i, Mod):
                mod += 1
            if isinstance(i, Copy):
                cpy += 1
        op = add + sub + div + mul + mod
        return 'add=%d sub=%d mul=%d div=%d mod=%d cpy=%d op=%d' % (add,sub,mul,div,mod,cpy,op)

#loop stack is just a list with the first element being the top
