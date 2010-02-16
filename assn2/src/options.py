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

class MajorOrder:
    ROW=1
    COL=2

class OutputLanguage:
    def __init__(self):
        raise NotImplementedError

class C99(OutputLanguage):
    def comment_begin():
        return "/*"

    def comment_end():
        return "*/"

    def index(rows, cols, i, j):
        return i * cols + j

    def major_order():
        return MajorOrder.ROW

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
