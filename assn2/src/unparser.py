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
from intrinsics import *

class VarMap:
    def __init__(self):
        self.vars = {}
        self.nextid = {}

    def __getitem__(self, key):
        if key in self.vars:
            return self.vars[key]

        i = self.nextid.get(key.var_type, 0)
        self.nextid[key.var_type] = i+1
        self.vars[key] = "%s%d" % (key.var_type, i)
        return self.vars[key]

class Unparser(object):
    def __init__(self):
        raise NotImplementedError

class C99(Unparser):
    def __init__(self):
        pass

    comment_begin = '/*'
    comment_end = '*/'

    vartype = {
        numbers.Complex  : 'complex double',
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

    def unparse_tuple(self, sym):
        v, i = sym
        return "%s[%s]" % (v, i)

    def unparse_index(self, sym):
        #map(lambda x: 'i' + str(x), range(self.istack-1, -1, -1))
        idx = sym.idx(self.istack)
        return self.unparse_tuple(idx)

    def unparse_complex(self, sym):
        """Complex values are of the form 'real + imag * I' in C99."""
        #TODO should really check the codetype first
        return "(%f+%f*I)" % (sym.real, sym.imag)

    def unparse_var(self, sym):
        if isinstance(sym, IRef):
            return self.istack[sym.val]

        v = self.varmap[sym]
        if isinstance(sym, VarF):
            self.typemap[v] = C99.vartype[self.codetype]
        else:
            self.typemap[v] = C99.vartype[numbers.Integral]
        return v

    def unparse_intrinsic(self, sym):
        #TODO UGLY!
        s = sym.__class__.__name__ + '('
        hasarg = False
        if hasattr(sym, 'mn'):
            if hasarg:
                s += ', '
            s += str(self.unparse_sym(sym.mn))
            hasarg = True
        if hasattr(sym, 'n'):
            if hasarg:
                s += ', '
            s += str(self.unparse_sym(sym.n))
            hasarg = True
        if hasattr(sym, 'k'):
            if hasarg:
                s += ', '
            s += str(self.unparse_sym(sym.k))
            hasarg = True
        s += ')'

        return s

    def unparse_sym(self, sym):
        if isinstance(sym, numbers.Real):
            return sym
        elif isinstance(sym, numbers.Complex):
            return self.unparse_complex(sym)
        elif isinstance(sym, tuple):
            return self.unparse_tuple(sym)
        elif isinstance(sym, Index):
            return self.unparse_index(sym)
        elif isinstance(sym, Var):
            return self.unparse_var(sym)
        elif isinstance(sym, Intrinsic):
            return self.unparse_intrinsic(sym)
        raise TypeError

    def op(self, dest, src1, op, src2):
        return "%s = %s %s %s;" % (self.unparse_sym(dest),
                                   self.unparse_sym(src1),
                                   C99.sym[op],
                                   self.unparse_sym(src2))

    def copy(self, dest, src1):
        return "%s = %s;" % (self.unparse_sym(dest),
                             self.unparse_sym(src1))

    #TODO have to get comments working!
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

        self.typemap = {}
        self.varmap = VarMap()

        src = []
        self.istack = []

        #TODO implement the rest of these
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
                self.istack.insert(0, "i%d" % len(self.istack))
                src.append("for (size_t %s = 0; %s < %d; %s++) {"
                           % (self.istack[0], self.istack[0], i.src1, self.istack[0]))
            elif isinstance(i, icode.End):
                src.append("}")
                self.istack = self.istack[1:]
            elif isinstance(i, icode.DefTmp):
                pass

        defs = ["%s %s;" % (self.typemap[i], i) for i in self.typemap]
        src = defs + src

        #Indent the source lines
        src = ['\t' + i for i in src]

        src.insert(0, "void %s(%s *y, %s *x) {" % (opt.next_name(), datastr, datastr))
        src.append("}")
        return '\n'.join(src)
