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

def num(sym):
    if isinstance(sym, numbers.Number):
        return sym

    if isinstance(sym, Intrinsic):
        if not isnum_or_none(num(sym.mn)) or not isnum_or_none(num(sym.n)) or not isnum_or_none(num(sym.k)):
            return sym

    if hasattr(sym, 'num'):
        return sym.num()
    return sym
    #raise NameError

def isnum_or_none(sym):
    return isinstance(sym, numbers.Number) or sym is None

def isnumeric(sym):
    return isinstance(sym, numbers.Number)

def isindex(sym):
    return isinstance(sym, tuple) or isinstance(sym, Index)

class ICodeList:
    def __init__(self, icode):
        self.icode = icode

    def varunroll(self, old, stack, varmap, outvar=False):
        if old is None:
            return None
        if isnumeric(old):
            return old
        elif isinstance(old, Intrinsic):
            new = copy.copy(old)
            new.mn = self.varunroll(new.mn, stack, varmap, False)
            new.n = self.varunroll(new.n, stack, varmap, False)
            new.k = self.varunroll(new.k, stack, varmap, False)
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
            return stack[old.ref].val
        #We want to do SSA. If we are an output variable, create
        #a new map. Otherwise we want to use our old value.
        elif outvar:
            varmap[old] = old.__class__(old.val, old.name)
            return varmap[old]
        elif old in varmap:
            return varmap[old]
        else:
            return old

    def inline_calls(self):
        processed = []
        for inst in self.icode:
            if isinstance(inst, Call):
                newil = inst.src1(inst.src2, inst.dest)
                newil.inline_calls()
                # print "INST:::", inst
                # print "NEWLIL:::", newil
                processed.extend(newil.icode)
            elif isinstance(inst, DefTmp):
                pass
            else:
                processed.append(inst)
        self.icode = processed

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
                stack.insert(0, DoVar(i,num(inst.src1)))
                #print 'DoVar: ', i, inst, num(inst.src1), stack
            elif isinstance(inst, End):
                stack[0].val += 1
                #if < then we still have to loop, otherwise move on
                if stack[0].val < stack[0].n:
                    #iold = i
                    i = stack[0].inst
                    #print 'End: ', iold, '->', i, stack
                else:
                    #print 'End: ', i, '(Stop)', stack
                    stack = stack[1:]

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
                        self.icode[i] = None
                    elif src2 == 0:
                        inst.dest.val = src1
                        self.icode[i] = None

                elif isinstance(inst, Mul):
                    if isnumeric(src1) and isnumeric(src2):
                        if isinstance(inst.dest, tuple):
                            self.icode[i] = Copy(src1 * src2, inst.dest)
                        else:
                            inst.dest.val = src1 * src2
                            self.icode[i] = None
                    elif src1 == 1:
                        if isinstance(inst.dest, tuple):
                            self.icode[i] = Copy(src2, inst.dest)
                        else:
                            inst.dest.val = src2
                            self.icode[i] = None
                    elif src2 == 1:
                        if isinstance(inst.dest, tuple):
                            self.icode[i] = Copy(src1, inst.dest)
                        else:
                            inst.dest.val = src1
                            self.icode[i] = None
                    elif src1 == 0 or src2 == 0:
                        if isinstance(inst.dest, tuple):
                            self.icode[i] = Copy(src1, inst.dest)
                        else:
                            inst.dest.val = 0
                            self.icode[i] = None

                elif isinstance(inst, Div):
                    if isnumeric(src1) and isnumeric(src2):
                        inst.dest.val = src1 / src2
                        self.icode[i] = None
                    elif src1 == 0:
                        inst.dest.val = 0
                        self.icode[i] = None
                    elif src2 == 1:
                        inst.dest.val = src1
                        self.icode[i] = None
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
                    if not isindex(src1):
                        if not isindex(inst.dest):
                            if isinstance(src1, numbers.Number):
                                inst.dest.val = src1
                            else:
                                print i, inst
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
        add = sum([1 for i in self.icode if isinstance(i, Add)])
        sub = sum([1 for i in self.icode if isinstance(i, Sub)])
        mul = sum([1 for i in self.icode if isinstance(i, Mul)])
        div = sum([1 for i in self.icode if isinstance(i, Div)])
        mod = sum([1 for i in self.icode if isinstance(i, Mod)])
        cpy = sum([1 for i in self.icode if isinstance(i, Copy)])
        do = sum([1 for i in self.icode if isinstance(i, Do)])
        op = add + sub + div + mul + mod
        return 'add=%d sub=%d mul=%d div=%d mod=%d cpy=%d op=%d do=%d' % (add,sub,mul,div,mod,cpy,op,do)

#loop stack is just a list with the first element being the top
