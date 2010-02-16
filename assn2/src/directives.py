#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

directives.py

Contains all of the runtime directives that can be set.
"""

import numbers

class Directives:
    def __init__(self):
        self.unroll = False
        self.optimize = False
        self.verbose = False
        self.debug = False
        self.internal = False
        self.subname = "func"
        self.codetype = numbers.Real
        self.datatype = numbers.Real
