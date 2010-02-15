#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

icode_parser.py

I-Code Parser
"""

import ply.lex as lex
import ply.yacc as yacc

import iast

class ICodeParser:
  def __init__(self, debug=False):
    self.debug = debug
    modname = self.__class__.__name__
    self.debugfile = modname + ".dbg"
    self.tabmodule = modname + "_parsetab"

    #Build the lexer and parser
    self.lexer = lex.lex(module=self, debug=self.debug)
    self.parser = yacc.yacc(module=self, debug=self.debug,
        debugfile=self.debugfile, tabmodule=self.tabmodule)

    def parse(self, data):
      return yacc.parse(data)

    def lexer_test(self, data):
      self.lexer.input(data)
      for tok in self.lexer:
        print tok

    #### LEX ##################################################################

    precedence = ()

    tokens =  

