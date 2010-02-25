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

class OutputLanguage(object):
    def __init__(self):
        raise NotImplementedError

class C99(OutputLanguage):
    def __init__(self):
        pass

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
            return sym
        print sym
        return self.nxt[sym]

    def op(self, dest, src1, op, src2):
        return "%s = %s %s %s;" % (self.var(dest), self.var(src1), C99.sym[op], self.var(src2))

    def copy(self, dest, src1):
        return "%s = %s;" % (self.var(dest), self.var(src1))

    def comment(self, str):
        return "%s %s %s" % (C99.comment_begin, str, C99.comment_end)

    def write_function(self, opt, il):
        codetype = opt.codetype
        datatype = opt.datatype

        #If our code is complex then we have to have complex input
        if codetype == numbers.Complex:
            datatype = codetype

        codestr = C99.vartype[codetype]
        datastr = C99.vartype[datatype]

        self.nxt = NextVarSet()

        src = []
        src.append("void %s(%s *y, %s *x) {" % (opt.next_name(), codestr, codestr))

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

        src.append("}")
        return '\n'.join(src)
