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

import sys
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
      'SCALAR', 'VECTOR', 'DOUBLE', 'INTEGER', 'EQUALS',
      'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
      'CALL', 'SPLNAME', 'DO', 'END',
      'NEWTMP', 'COMMENT', 'LBRACKET', 'RBRACKET', 'DOLLAR'
      )

  KEYWORDS = {
      "do"        : "DO",
      "end"       : "END",
      "newtmp"    : "NEWTMP",
      "call"      : "CALL",
  }

  t_EQUALS = r'='
  t_MINUS = r'-'
  t_PLUS = r'\+'
  t_MULT = r'\*'
  t_DIV = r'/'
  t_MOD = r'%'
  t_LBRACKET = r'\['
  t_RBRACKET = r'\]'
  t_DOLLAR = r'\$'

  def t_COMMENT(self, t):
    r';.*'
    t.value = t.value[1:]
    return t

  def t_DOUBLE(self,t):
    r"""(\d+(\.\d*)|\.\d+)([eE][-+]?\d+)?""" #This is a much better decimal
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

  def t_SCALAR(self, t):
    r'[rfip]\d+'
    return t

  def t_VECTOR(self, t):
    r'[xy]|t\d+'
    return t

  def t_SYMBOL(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = self.KEYWORDS.get(t.value.lower(), "SPLNAME")
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
    """stmt : add
            | sub
            | mul
            | div
            | mod
            | assn
            | call
            | do
            | newtmp
            | comment"""
    p[0] = p[1]

  def p_value(self, p):
    """value : DOUBLE
             | INTEGER
             | symbol"""
    p[0] = p[1]

  def p_symbol(self, p):
    """symbol : DOLLAR SCALAR
              | DOLLAR VECTOR"""
    p[0] = iast.Symbol(p[1])

  def p_symbol_subscript(self, p):
    'symbol : VECTOR subscript'
    p[0] = iast.Symbol(p[1], p[2])

  def p_subscript(self, p):
    'subscript : LBRACKET value RBRACKET'
    p[0] = p[2]

  def p_comment(self, p):
    'comment : COMMENT'
    p[0] = iast.Comment(p[1])

  def p_add(self, p):
    'add : symbol EQUALS value PLUS value'
    p[0] = iast.Add(p[1], p[3], p[5])

  def p_sub(self, p):
    'sub : symbol EQUALS value MINUS value'
    p[0] = iast.Subtract(p[1], p[3], p[5])

  def p_mul(self, p):
    'mul : symbol EQUALS value MULT value'
    p[0] = iast.Multiply(p[1], p[3], p[5])

  def p_div(self, p):
    'div : symbol EQUALS value DIV value'
    p[0] = iast.Divide(p[1], p[3], p[5])

  def p_mod(self, p):
    'mod : symbol EQUALS value MOD value'
    p[0] = iast.Modulus(p[1], p[3], p[5])

  def p_assn(self, p):
    'assn : symbol EQUALS value'
    p[0] = iast.Assign(p[1], p[3])

  def p_call(self, p):
    'call : symbol EQUALS CALL SPLNAME'
    p[0] = iast.Call(p[1], p[4])

  def p_call_arg(self, p):
    'call : symbol EQUALS CALL SPLNAME symbol'
    p[0] = iast.Call(p[1], p[4], p[5])

  def p_do(self, p):
    'do : DO value stmt_list END DO'
    p[0] = iast.Do(p[2], p[3])

  def p_newtmp(self, p):
    'newtmp : NEWTMP value'
    p[0] = iast.NewTmp(p[2])

  def p_error(self, p):
    if p is not None:
      print "Line %s: Syntax error at '%s' (type = %s)" % (p.lineno, p.value, p.type)
    return None

def main():
  data = sys.stdin.read()
  parser = ICodeParser(debug=True)

  parser.lexer_test(data)

  t = parser.parse(data)
  print t

if __name__ == "__main__":
  sys.exit(main())
