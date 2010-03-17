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

import copy

#TODO Need to keep track of a LoopIdx stack
#TODO Need to keep track of a Temp stack

TOLERANCE = 1e-10
def feq(a,b):
    return abs(a-b) < TOLERANCE

def promote_complex(val):
    """If a complex value's imaginary value is negligable, it is promoted to a
    simple real or integer value"""
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

def isequal(a,b):
    if isinstance(a, tuple) and isinstance(b, tuple):
        if len(a) == len(b):
            for i in xrange(len(a)):
                if a[i] is not b[i]:
                    return False
            return True
    return False

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

def process_sub(src, v, sub):
    if isinstance(src, tuple):
        a,b = src
        if a is v:
            return (v, sub.index(b))
    return src

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
                    idx = list(old.idx(stack))
                    new = [ self.varunroll(i, stack, varmap, False) for i in idx[1:] ]
                    new.insert(0, idx[0])
                    return tuple(new)
            return old
        elif isinstance(old, DoVar):
            raise TypeError
        elif isinstance(old, IRef):
            return stack[old.ref].val
        elif isinstance(old, tuple):
            #TODO do we want to do this?
            #print "IREF: ", old
            return old
        #We want to do SSA. If we are an output variable, create
        #a new map. Otherwise we want to use our old value.
        elif isinstance(old, A):
            x = self.varunroll(old.x, stack, varmap, False)
            y = self.varunroll(old.y, stack, varmap, False)
            return old.node.a(x,y)
        elif outvar:
            varmap[old] = old.__class__(old.val, old.name)
            return varmap[old]
        elif old in varmap:
            return varmap[old]
        else:
            return old

    def process_subvectors(self, vec, sub):
        assert isinstance(sub, SubVector)

        for inst in self.icode:
            inst.src1 = process_sub(inst.src1, vec, sub)
            if hasattr(inst, 'src2'):
                inst.src2 = process_sub(inst.src2, vec, sub)
            inst.dest = process_sub(inst.dest, vec, sub)

    def inline_calls(self, symtab, options):
        processed = []
        for inst in self.icode:
            if isinstance(inst, Call):
                x = inst.src2
                y = inst.dest
                if isinstance(inst.src2, tuple):
                    x = inst.src2[0]
                if isinstance(inst.dest, tuple):
                    y = inst.dest[0]

                inst.src1.x = x
                inst.src1.y = y

                newil = inst.src1.evaluate(symtab, options)
                newil.unroll()
                newil.inline_calls(symtab, options)

                #print "Before PROCESSING:"
                #print "Src2: ", inst.src2
                #print "Dest: ", inst.dest
                #print "IL:\n", newil
                if isinstance(inst.src2, tuple):
                    newil.process_subvectors(x, inst.src2[1])

                if isinstance(inst.dest, tuple):
                    newil.process_subvectors(y, inst.dest[1])

                #print "After PROCESSING:\n", newil, "\n"

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
            if isinstance(inst, Do) or isinstance(inst, DoUnroll):
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
            elif isinstance(inst, Call):
                src1 = self.varunroll(inst.src1, stack, varmap, False)
                src2 = self.varunroll(inst.src2, stack, varmap, False)
                dest = self.varunroll(inst.dest, stack, varmap, True)
                unrolled.append(Call(src1, src2, dest))
            i+=1

        self.icode = unrolled

    def constprop(self):
        Var.next_val = NextVarSet()

        varmap = {}

        for i in xrange(len(self.icode)):
            inst = self.icode[i]

            #print "Propagating: ", inst

            #If an index tuple is of length 3 (when we have 'x(r0 1)') we
            #need to reduce to 2
            if hasattr(inst, 'src1') and isinstance(inst.src1, tuple) and len(inst.src1) > 2:
                inst.src1 = tuple([inst.src1[0], sum(inst.src1[1:])])
            if hasattr(inst, 'src2') and isinstance(inst.src2, tuple) and len(inst.src2) > 2:
                inst.src2 = tuple([inst.src2[0], sum(inst.src2[1:])])
            if hasattr(inst, 'dest') and isinstance(inst.dest, tuple) and len(inst.dest) > 2:
                inst.dest = tuple([inst.dest[0], sum(inst.dest[1:])])

            if isinstance(inst, OpICode):
                #src1 = num(inst.src1)
                #src2 = num(inst.src2)

                src1 = varmap.get(inst.src1, num(inst.src1))
                src2 = varmap.get(inst.src2, num(inst.src2))

                if isinstance(src1, numbers.Complex):
                    src1 = promote_complex(src1)
                if isinstance(src2, numbers.Complex):
                    src2 = promote_complex(src2)
                #print inst.__class__.__name__, src1, src2

                if src1:
                    inst.src1 = src1
                if src2:
                    inst.src2 = src2

                if isinstance(inst, Add):
                    if isnumeric(src1) and isnumeric(src2):
                        varmap[inst.dest] = src1 + src2
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src1 == 0:
                        varmap[inst.dest] = src2
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src2 == 0:
                        varmap[inst.dest] = src1
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    else:
                        if inst.dest in varmap:
                            del varmap[inst.dest]
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = None

                elif isinstance(inst, Sub):
                    if isnumeric(src1) and isnumeric(src2):
                        varmap[inst.dest] = src1 - src2
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src2 == 0:
                        varmap[inst.dest] = src1
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    else:
                        if inst.dest in varmap:
                            del varmap[inst.dest]
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = None

                elif isinstance(inst, Mul):
                    if isnumeric(src1) and isnumeric(src2):
                        varmap[inst.dest] = src1 * src2
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src1 == 1:
                        varmap[inst.dest] = src2
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src2 == 1:
                        varmap[inst.dest] = src1
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src1 == 0 or src2 == 0:
                        varmap[inst.dest] = 0
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    else:
                        if inst.dest in varmap:
                            del varmap[inst.dest]
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = None

                elif isinstance(inst, Div):
                    if isnumeric(src1) and isnumeric(src2):
                        varmap[inst.dest] = src1 / src2
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src1 == 0:
                        varmap[inst.dest] = 0
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src2 == 1:
                        varmap[inst.dest] = src1
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src2 == 0:
                        raise ZeroDivisionError
                    else:
                        if inst.dest in varmap:
                            del varmap[inst.dest]
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = None

                elif isinstance(inst, Mod):
                    if isnumeric(src1) and isnumeric(src2):
                        varmap[inst.dest] = src1 % src2
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src1 == 0 or src2 == 1:
                        varmap[inst.dest] = 0
                        self.icode[i] = Copy(varmap[inst.dest], inst.dest)
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = varmap[inst.dest]
                    elif src2 == 0:
                        raise ZeroDivisionError
                    else:
                        if inst.dest in varmap:
                            del varmap[inst.dest]
                        if not isinstance(inst.dest, tuple):
                            inst.dest.val = None

            elif isinstance(inst, Copy):
                inst.src1 = varmap.get(inst.src1, num(inst.src1))
                varmap[inst.dest] = inst.src1
                if not isinstance(inst.dest, tuple):
                    inst.dest.val = inst.src1

        #Remove any None placeholders
        self.icode = [i for i in self.icode if i is not None]

    def cse(self):
        """Common Subexpression Elimination. see 'Advanced Compiler Design &
        Implementation' by Steven Muchinich"""
        pass

    def propnegs(self):
        #This a map from destinations to the assigned expressions
        subexp = {}

        for i in xrange(len(self.icode)):
            inst = self.icode[i]

            if isinstance(inst, OpICode):
                s1 = subexp.get(inst.src1, inst.src1)
                if not isinstance(s1, OpICode):
                    inst.src1 = s1

                s2 = subexp.get(inst.src2, inst.src2)
                if not isinstance(s2, OpICode):
                    inst.src2 = s2

                #Clear out the unneccessary instruction, because we do not need the value anymore
                if inst.dest in subexp:
                    if inst.dest != inst.src1 and inst.dest != inst.src2:
                        del subexp[inst.dest]

                subexp[inst.dest] = inst.__class__(inst.src1, inst.src2, None)

                if isinstance(inst, Add):
                    if inst.src1 in subexp:
                        x = subexp[inst.src1]
                        if isinstance(x, Mul):
                            if x.src1 == -1:
                                inst = Sub(inst.src2, x.src2, inst.dest)
                                subexp[inst.dest] = inst.__class__(inst.src1, inst.src2, None)
                            if x.src2 == -1:
                                inst = Sub(inst.src2, x.src1, inst.dest)
                                subexp[inst.dest] = inst.__class__(inst.src1, inst.src2, None)
                    if inst.src2 in subexp:
                        x = subexp[inst.src2]
                        if isinstance(x, Mul):
                            if x.src1 == -1:
                                del subexp[inst.src2]
                                inst = Sub(inst.src1, x.src2, inst.dest)
                                subexp[inst.dest] = inst.__class__(inst.src1, inst.src2, None)
                            elif x.src2 == -1:
                                del subexp[inst.src1]
                                inst = Sub(inst.src2, x.src1, inst.dest)
                                subexp[inst.dest] = inst.__class__(inst.src1, inst.src2, None)

            self.icode[i] = inst

        #Remove any None placeholders
        self.icode = [i for i in self.icode if i is not None]

    def dca(self):
        #maps the variables to the line they are last used in
        varmap = {}

        #keeps track of whether an outvariable was already set
        outmap = {}

        for i in reversed(xrange(len(self.icode))):
            inst = self.icode[i]

            if inst.dest in varmap or (isinstance(inst.dest, tuple) and inst.dest not in outmap):
                if isinstance(inst.dest, tuple):
                    outmap[inst.dest] = i
                    #print "OUTMAP: ", outmap
                if hasattr(inst, 'src1') and not isinstance(inst.src1, numbers.Number):
                    varmap[inst.src1] = i
                if hasattr(inst, 'src2') and not isinstance(inst.src2, numbers.Number):
                    varmap[inst.src2] = i
                if inst.dest in varmap:
                    if not (hasattr(inst, 'src1') and isequal(inst.src1, inst.dest)) and not (hasattr(inst, 'src2') and isequal(inst.src2, inst.dest)):
                        del varmap[inst.dest]
                #print "VARMAP: ", inst, varmap
            else:
                self.icode[i] = None
        self.icode = [i for i in self.icode if i is not None]


    def split_temp_arrays(self):
        varmap = {}
        for i in xrange(len(self.icode)):
            inst = self.icode[i]
            if hasattr(inst, 'src1'):
                if inst.src1 in varmap:
                    inst.src1 = varmap[inst.src1]
                elif isinstance(inst.src1, tuple):
                    if isinstance(inst.src1[0], Vec) and not isinstance(inst.src1[0], IOVec):
                        varmap[inst.src1] = VarF()
                        inst.src1 = varmap[inst.src1]
            if hasattr(inst, 'src2'):
                if inst.src2 in varmap:
                    inst.src2 = varmap[inst.src2]
                elif isinstance(inst.src2, tuple):
                    if isinstance(inst.src2[0], Vec) and not isinstance(inst.src2[0], IOVec):
                        varmap[inst.src2] = VarF()
                        inst.src2 = varmap[inst.src2]
            if hasattr(inst, 'dest'):
                if inst.dest in varmap:
                    inst.dest = varmap[inst.dest]
                elif isinstance(inst.dest, tuple):
                    if isinstance(inst.dest[0], Vec) and not isinstance(inst.dest[0], IOVec):
                        varmap[inst.dest] = VarF()
                        inst.dest = varmap[inst.dest]

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
