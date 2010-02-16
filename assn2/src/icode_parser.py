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

  tokens = (
      'SYMBOL', 'DOUBLE', 'INTEGER', 'EQUALS',
      'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
      'CALL', 'SPLNAME', 'DO', 'END',
      'NEWTMP', 'COMMENT' 

      )

  t_MINUS = r'-'
  t_PLUS = r'\+'
  t_MULT = r'\*'
  t_DIV = r'/'
  t_MOD = r'%'

  def t_COMMENT(self, t):
    r';.*'
    t.value = t.value[1:]
    return t


  def t_DOUBLE(self,t):
      r"""(\d+(\.\d*)|\.\d+)([eE][-+]?\d+)?""" #This is a much better decimal number
      try:
          t.value = float(t.value)
      except ValueError:
          print "Value incorrect: ", t.value
          t.value = float('nan')
      return t

  def t_INTEGER(self,t):
      r'\d+'
      try:
          t.value = int(t.value)
      except ValueError:
          print "Value incorrect: ", t.value
          t.value = 0
      return t

  def t_SYMBOL(self, t):
      r'[a-zA-Z_][a-zA-Z0-9_]*'
      t.type = self.RESERVED.get(t.value, "SYMBOL")
      return t

  # Define a rule so we can track line numbers
  def t_newline(self,t):
      r'\n+'
      t.lexer.lineno += len(t.value)

  t_ignore = ' \t'

  # Error handling rule
  def t_error(self,t):
      print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
      return t

  #### YACC ###################################################################

  def p_program(self, p):
    'program : stmt_list'
    p[0] = iast.Program(p[1])

  def p_stmt_list(self, p):
    'stmt_list : stmt stmt_list'
    p[2].prepend(p[1])
    p[0] = p[2]

  def p_stmt_list_tail(self, p):
    'stmt_list : stmt'
    p[0] = iast.StmtList(p[1])

  def p_stmt(self, p):
    """stmt : add \n
            | sub \n
            | mul \n
            | div \n
            | mod \n
            | assn \n
            | call \n
            | do \n
            | newtmp \n"""
    p[0] = p[1]


