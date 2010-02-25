#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

options.py

Contains all of the compile time and runtime evaluation options.
"""

import numbers
import icode
import sys

class MajorOrder:
    ROW=1
    COL=2

class OutputLanguage:
    def __init__(self):
        raise NotImplementedError

class NextVarSet:
    def __init__(self):
        self.vars = {}

    def __getitem__(self, key):
        if key not in self.vars:
            self.vars[key] = 0
        i = self.vars[key]
        self.vars[key] += 1
        return "%s%d" % (key, i)

class C99(OutputLanguage):
    def __init__(self):
        pass

    def comment_begin():
        return "/*"

    def comment_end():
        return "*/"

    def index(rows, cols, i, j):
        return i * cols + j

    def major_order():
        return MajorOrder.ROW

    def printop(file, dest, src1, op, src2):
        print >>file, "%s = %s %s %s" % (nxt[dest], nxt[src1], op, nxt[src2])

    def output(options, icode, file=sys.stdout):
        name = options.next_name()
        print >>file, "void %s(%s *y, %s *x) {" % (name, "complex", "complex")

        nxt = NextVarSet()
        for i in icode:
            if isinstance(i, icode.Add):
                printop(file, i.dest, i.src1, '+', i.src2)
            elif isinstance(i, icode.Sub):
                printop(file, i.dest, i.src1, '-', i.src2)
            elif isinstance(i, icode.Mul):
                printop(file, i.dest, i.src1, '*', i.src2)
            elif isinstance(i, icode.Div):
                printop(file, i.dest, i.src1, '/', i.src2)
            elif isinstance(i, icode.Mod):
                printop(file, i.dest, i.src1, '%', i.src2)
            elif isinstance(i, icode.Copy):
                pass
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

        print >>file, "}"

class Options:
    def __init__(self):
        self.unroll = True
        self.optimize = True
        self.verbose = False
        self.debug = False
        self.internal = False
        self.subname = "func"
        self.codetype = numbers.Real
        self.datatype = numbers.Complex
        self.language = C99
        self.sign = 1
        self.next = {}

    def __getitem__(self, key):
        try:
            getattr(self, key)
        except:
            raise KeyError

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        raise KeyError

    def __delitem__(self, key):
        raise KeyError

    def next_name(self):
        if self.subname not in self.next:
            self.next[self.subname] = 0
            return self.subname
        self.next[self.subname] += 1
        return "%s_%d" % (self.subname, self.next[self.subname])
