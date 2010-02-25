#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

options.py Contains all of the compile time and runtime evaluation options.
"""

import numbers

class Options:
    def __init__(self):
        self.unroll = True
        self.optimize = True
        self.verbose = False
        self.debug = False
        self.internal = False

        #datatype is the type of the input / output vectors
        self.datatype = numbers.Complex

        #codetype is the type used in the target language
        self.codetype = numbers.Complex

        self.language = C99
        self.sign = 1

        #Keeps track of the current function name and which ones are already
        #used
        self.subname = "func"
        self._next = {}

    def next_name(self):
        if self.subname not in self._next:
            self._next[self.subname] = 0
            return self.subname
        self._next[self.subname] += 1
        return "%s_%d" % (self.subname, self._next[self.subname])

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
