#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

flags.py

Contains all of the runtime flags that can be set.
"""

class Flags:
    def __init__(self):
        self.unroll = False
        self.optimize = False
        self.verbose = False
        self.debug = False
        self.internal = False
        self.subname = "func"
