#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

parser.py

SPL Parser
"""

import ply.lex as lex
import ply.yacc as yacc

import ast

class MiniParser:
    def __init__(self,debug=False):
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

    def lexer_test(self,data):
        self.lexer.input(data)
        for tok in self.lexer:
            print tok

    ##### LEX #################################################################

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIV', 'MOD'),
        ('right','UMINUS')
    )

    # List of token names.	 This is always required
    tokens = (
        'MATRIX', 'DIAGONAL', 'PERMUTATION', 'RPERMUTATION', 'SPARSE',
        'I', 'J', 'O', 'F', 'L', 'T',
        'COMPOSE', 'TENSOR', 'DIRECT_SUM', 'CONJUGATE', 'SCALE',
        'DEFINE', 'UNDEFINE',
        'SUBNAME', 'DATATYPE', 'CODETYPE', 'UNROLL', 'VERBOSE', 'DEBUG', 'INTERNAL',
    )

    # dictionary of reserved words
    RESERVED = {
        "C"         :	"C",
        "S"         :	"S",
        "TW"        :	"TW",
        "TWI"       :	"TWI",
        "TWR"       :	"TWR",
        "W"         :	"W",
        "WI"        :	"WI",
        "WR"        :	"WR",
        "alias"     :	"ALIAS",
        "any"       :	"ANYNODE",
        "call"      :	"CALL",
        "codetype"  :	"CODETYPE",
        "complex"   :	"COMPLEX",
        "cos"       :	"COS",
        "datatype"  :	"DATATYPE",
        "debug"     :	"DEBUG",
        "def"       :	"DEFINE",
        "define"    :	"DEFINE",
        "define_"   :	"DEFINE_",
        "deftemp"   :	"DEFTEMP",
        "direct"    :	"DIRECT",
        "div"       :	"DIV",
        "do"        :	" LOOP",
        "dounroll"  :	"LOOPUNROLL",
        "end"       :	"LOOPEND",
        "exp"       :	"EXP",
        "internal"  :	"INTERNAL",
        "log"       :	"LOG",
        "misc"      :	"MISC",
        "mod"       :	"MOD",
        "off"       :	"OFF",
        "on"        :	" ON",
        "operation" :	"OPERATION",
        "optimize"  :	"OPTIMIZE",
        "pi"        :	" PI",
        "primitive" :	"PRIMITIVE",
        "real"      :	"REAL",
        "recursive" :	"RECURSIVE",
        "slef"      :	"SELFNODE",
        "sin"       :	"SIN",
        "sqrt"      :	"SQRT",
        "subname"   :	"SUBNAME",
        "tan"       :	"TAN",
        "template"  :	"TEMPLATE",
        "undef"     :	"UNDEFINE",
        "undefine"  :	"UNDEFINE",
        "unroll"    :	"UNROLL",
        "verbose"   :	"VERBOSE",
        "w"         :	"ROOT_OF_ONE",
    }

    t_VAR_X = r'$x'
    t_VAR_Y = r'$y'
    t_VAR_F = r'$f[0-9]+'
    t_VAR_I = r'$i[0-9]+'
    t_VAR_R = r'$r[0-9]+'
    t_VAR_T = r'$t[0-9]+'
    t_VAR_P = r'$p[0-9]+'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COMMENT = r';'
    t_DIRECTIVE = r'\#'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','

    t_EQUALS = r'='
    t_PLUS = r'+'
    t_MINUS = r'-'
    t_MULT = r'*'
    t_DIV = r'/'
    t_MOD = r'%'
    t_UMINUS = r'-'

    def t_INVISIBLE_COMMENT(self, t):
        r';;.*'
        pass

    def t_COMMENT(self, t):
        r';.*'
        return t[1:]

    def t_DOUBLE(self,t):
        r"""(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?""" #This is a much better decimal number
        try:
            t.value = float(t.value)
        except ValueError:
            print "Value incorrect: ", t.value
            t.value = float('nan')
        return t

    def t_INT(self,t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print "Value incorrect: ", t.value
            t.value = 0
        return t

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.RESERVED.get(t.value.lower(), "IDENT")
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
        return t
        #t.lexer.skip(1)

    ##### YACC ################################################################

#     def p_program(self, p):
#         'program : stmt_list'
#         p[0] = ast.ProgramNode(p[1])

#     def p_stmt_list(self, p):
#         'stmt_list : stmt SEMICOLON stmt_list'
#         p[3].prepend(p[1])
#         p[0] = p[3]

#     def p_stmt_list_tail(self, p):
#         'stmt_list : stmt'
#         p[0] = ast.StmtListNode(p[1])

#     def p_stmt(self, p):
#         """stmt : assign_stmt
#             | define_stmt
# 				| if_stmt
# 				| while_stmt
# 				| repeat_stmt
# 				| return_stmt"""
# 		p[0] = p[1]

# 	def p_assign_stmt(self, p):
# 		'assign_stmt : IDENT ASSIGN expr'
# 		p[0] = ast.AssignNode(p[1], p[3])

# 	def p_define_stmt(self, p):
# 		'define_stmt : DEFINE IDENT PROC LPAREN param_list RPAREN stmt_list END'
# 		p[0] = ast.DefineNode(p[2], p[5], p[7])

# 	def p_if_stmt(self, p):
# 		'if_stmt : IF expr THEN stmt_list ELSE stmt_list FI'
# 		p[0] = ast.IfNode(p[2], p[4], p[6])

# 	def p_while_stmt(self, p):
# 		'while_stmt : WHILE expr DO stmt_list OD'
# 		p[0] = ast.WhileNode(p[2], p[4])

# 	def p_repeat_stmt(self, p):
# 		'repeat_stmt : REPEAT stmt_list UNTIL expr'
# 		p[0] = ast.RepeatNode(p[2], p[4])

# 	def p_return_stmt(self, p):
# 		'return_stmt : RETURN expr'
# 		p[0] = ast.ReturnNode(p[2])

# 	def p_param_list(self, p):
# 		'param_list : IDENT COMMA param_list'
# 		p[3].prepend(p[1])
# 		p[0] = p[3]

# 	def p_param_list_tail(self, p):
# 		'param_list : IDENT'
# 		p[0] = ast.ParamListNode(p[1])

# 	def p_expr_plus(self, p):
# 		'expr : expr PLUS term'
# 		p[0] = ast.AddNode(p[1], p[3])

# 	def p_expr_minus(self, p):
# 		'expr : expr MINUS term'
# 		p[0] = ast.SubNode(p[1], p[3])

# 	def p_expr_lcat(self, p):
# 		'expr : expr LCAT expr'
# 		p[0] = ast.LcatNode(p[1], p[3])

# 	def p_expr_term(self, p):
# 		'expr : term'
# 		p[0] = p[1]

# 	def p_term(self, p):
# 		'term : term MULT factor'
# 		p[0] = ast.MulNode(p[1], p[3])

# 	def p_term_factor(self, p):
# 		'term : factor'
# 		p[0] = p[1]

# 	def p_factor_expr(self, p):
# 		'factor : LPAREN expr RPAREN'
# 		p[0] = p[2]

# 	def p_factor_proc(self, p):
# 		'factor : proc'
# 		p[0] = p[1]

# 	def p_factor_list(self, p):
# 		'factor : list'
# 		p[0] = p[1]

# 	def p_factor_number(self, p):
# 		'factor : NUMBER'
# 		p[0] = ast.NumNode(p[1])

# 	def p_factor_ident(self, p):
# 		'factor : IDENT'
# 		p[0] = ast.VarNode(p[1])

# 	def p_list_empty(self, p):
# 		'list : LBRACKET RBRACKET'
# 		p[0] = ast.ListNode()

# 	def p_list(self, p):
# 		'list : LBRACKET sequence RBRACKET'
# 		p[0] = ast.ListNode(p[2])

# 	def p_sequence(self, p):
# 		'sequence : expr COMMA sequence'
# 		p[3].insert(0, p[1])
# 		p[0] = p[3]

# 	def p_sequence_tail(self, p):
# 		'sequence : expr'
# 		p[0] = [p[1]]

# 	def p_factor_funcall(self, p):
# 		'factor : funcall'
# 		p[0] = p[1]

# #	def p_funcall(self, p):
# #		'funcall : IDENT LPAREN expr_list RPAREN'
# #		p[0] = ast.CallNode(p[1], p[3])

# 	def p_funcall_proc(self, p):
# 		'funcall : factor LPAREN expr_list RPAREN'
# 		p[0] = ast.CallNode(p[1], p[3])

# 	def p_proc(self, p):
# 		'proc : PROC LPAREN param_list RPAREN stmt_list END'
# 		p[0] = ast.ProcNode(p[3], p[5])

# 	def p_expr_list(self, p):
# 		'expr_list : expr COMMA expr_list'
# 		p[3].prepend(p[1])
# 		p[0] = p[3]

# 	def p_expr_list_tail(self, p):
# 		'expr_list : expr'
# 		p[0] = ast.ExprListNode(p[1])

# 	def p_error(self, p):
# 		if p is not None:
# 			print "Line: %s Syntax error at '%s'" % (p.lineno, p.value)
# 		return None
