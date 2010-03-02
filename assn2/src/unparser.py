#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

unparser.py Unparses icode into an output language
"""

import numbers
import icode
from options import Options
from symbols import *

class Unparser(object):
    def __init__(self):
        raise NotImplementedError

class C99(Unparser):

    def __init__(self):
        self.varmap = {}

    comment_begin = '/*'
    comment_end = '*/'

    vartype = {
        numbers.Complex  : 'complex',
        numbers.Real     : 'double',
        numbers.Integral : 'int',
        }

    sym = {
        icode.Add : '+',
        icode.Sub : '-',
        icode.Mul : '*',
        icode.Div : '/',
        icode.Mod : '%',
        }

    def var(self, sym):
        if isinstance(sym, numbers.Number):
            return "%s" % sym
        if isinstance(sym, tuple):
            v, i = sym
            return "%s[%s]" % (v, i)
        if isinstance(sym, Var):
            v = self.idmap[sym.var_type]
            if isinstance(sym, VarF):
                self.varmap[v] = C99.vartype[self.codetype]
            else:
                self.varmap[v] = C99.vartype[numbers.Integral]
            return v
        raise TypeError

    def op(self, dest, src1, op, src2):
        return "%s = %s %s %s;" % (self.var(dest), self.var(src1), C99.sym[op], self.var(src2))

    def copy(self, dest, src1):
        return "%s = %s;" % (self.var(dest), self.var(src1))

    def comment(self, str):
        return "%s %s %s" % (C99.comment_begin, str, C99.comment_end)

    def write_function(self, opt, il):
        self.codetype = opt.codetype
        self.datatype = opt.datatype

        #If our code is complex then we have to have complex input
        if self.codetype == numbers.Complex:
            self.datatype = self.codetype

        codestr = C99.vartype[self.codetype]
        datastr = C99.vartype[self.datatype]

        self.idmap = NextVarSet()

        src = []

        for i in il.icode:
            if isinstance(i, icode.OpICode):
                src.append(self.op(i.dest, i.src1, i.__class__, i.src2))
            elif isinstance(i, icode.Copy):
                src.append(self.copy(i.dest, i.src1))
            elif isinstance(i, icode.Call):
                pass
            elif isinstance(i, icode.DoUnroll):
                pass
            elif isinstance(i, icode.Do):
                pass
            elif isinstance(i, icode.End):
                pass
            elif isinstance(i, icode.DefTmp):
                pass

        defs = ["%s %s;" % (self.varmap[i], i) for i in self.varmap]
        src = defs + src

        #Indent the source lines
        src = ['\t' + i for i in src]

        src.insert(0, "void %s(%s *y, %s *x) {" % (opt.next_name(), datastr, datastr))
        src.append("}")
        return '\n'.join(src)
