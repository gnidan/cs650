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
    def __init__(self, unparser):
        self.unroll = True
        self.optimize = True
        self.verbose = False
        self.debug = False
        self.internal = False

        #datatype is the type of the input / output vectors
        self.datatype = numbers.Complex

        #codetype is the type used in the target language
        self.codetype = numbers.Complex
        self.sign = 1

        self.unparser = unparser

        #Keeps track of the current function name and which ones are already
        #used
        self.subname = "func"
        self._next = {}

    def next_name(self):
        """gets the next function name based on 'self.subname'"""
        if self.subname not in self._next:
            self._next[self.subname] = 0
            return self.subname
        self._next[self.subname] += 1
        return "%s_%d" % (self.subname, self._next[self.subname])

    def __getitem__(self, key):
        """allows options to be accessed by string name"""
        try:
            getattr(self, key)
        except:
            raise KeyError

    def __setitem__(self, key, value):
        """allows options to be set by string name"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError

    def __delitem__(self, key):
        """we don't want no delete"""
        raise KeyError
