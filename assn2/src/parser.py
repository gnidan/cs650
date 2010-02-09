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
        "do"        :	"LOOP",
        "dounroll"  :	"LOOPUNROLL",
        "end"       :	"LOOPEND",
        "exp"       :	"EXP",
        "internal"  :	"INTERNAL",
        "log"       :	"LOG",
        "misc"      :	"MISC",
        "mod"       :	"MOD",
        "off"       :	"OFF",
        "on"        :	"ON",
        "operation" :	"OPERATION",
        "optimize"  :	"OPTIMIZE",
        "pi"        :	"PI",
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

    t_PLUS = r'+'
    t_MINUS = r'-'
    t_MULT = r'*'
    t_DIV = r'/'
    t_RPAREN = r'\)'
    t_HASH = r'\#'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','

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

    def t_INTEGER(self,t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print "Value incorrect: ", t.value
            t.value = 0
        return t

    def t_symbol(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.RESERVED.get(t.value.lower(), "symbol")
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

    def p_program(self, p):
        'program : stmt_list'
        p[0] = ast.Program(p[1])

    def p_stmt_list(self, p):
        'stmt_list : stmt SEMICOLON stmt_list'
        p[3].prepend(p[1])
        p[0] = p[3]

    def p_stmt_list_tail(self, p):
        'stmt_list : stmt'
        p[0] = ast.StmtList(p[1])

    def p_stmt(self, p):
        """stmt : definition
                | directive
                | comment"""
        p[0] = p[1]

    def p_comment(self, p):
        'stmt : COMMENT'
        p[0] = ast.Comment(p[1])

    def p_directive_subname(self, p):
        'directive : HASH SUBNAME symbol'
        p[0] = ast.Subname(p[3])
        
    def p_directive_codetype(self, p):
        'directive : HASH CODETYPE type'
        p[0] = ast.Codetype(p[3])
        
    def p_directive_datatype(self, p):
        'directive : HASH DATATYPE type'
        p[0] = ast.Datatype(p[3])
        
    def p_directive_optimize(self, p):
        'directive : HASH OPTIMIZE flag'
        p[0] = ast.Optimize(p[3])
        
    def p_directive_unroll(self, p):
        'directive : HASH UNROLL flag'
        p[0] = ast.Unroll(p[3])
        
    def p_directive_debug(self, p):
        'directive : HASH DEBUG flag'
        p[0] = ast.Debug(p[3])
        
    def p_directive_verbose(self, p):
        'directive : HASH VERBOSE flag'
        p[0] = ast.Verbose(p[3])
        
    def p_directive_internal(self, p):
        'directive : HASH INTERNAL flag'
        p[0] = ast.Internal(p[3])

    def p_type(self, p):
        'type : REAL'
        p[0] = ast.RealType()

    def p_type(self, p):
        'type : COMPLEX'
        p[0] = ast.ComplexType()

    def p_flag(self, p):
        'flag : ON'
        p[0] = On(p[1])

    def p_flag(self, p):
        'flag : OFF'
        p[0] = Off(p[1])

    def p_definition_formula(self, p):
        'definition : DEFINE symbol formula'
        p[0] = ast.Define(p[2], p[3])

    def p_definition_value(self, p):
        'definition : DEFINE symbol number'
        p[0] = ast.Define(p[2], p[3])

    def p_undefine(self, p):
        'undefinition : UNDEFINE symbol number'
        p[0] = ast.Define(p[2], p[3])

    def p_number_add(self, p):
        'number : number PLUS number'
        p[0] = ast.Add(p[1], p[3])

    def p_number_sub(self, p):
        'number : number MINUS number'
        p[0] = ast.Sub(p[1], p[3])

    def p_number_mul(self, p):
        'number : number MULT number'
        p[0] = ast.Mul(p[1], p[3])

    def p_number_div(self, p):
        'number : number DIV number'
        p[0] = ast.Div(p[1], p[3])

    def p_number_mod(self, p):
        'number : number MOD number'
        p[0] = ast.Mod(p[1], p[3])

    def p_number_neg(self, p):
        'number : MINUS number %prec UMINUS'
        p[0] = Neg(p[2])

    def p_number_paren(self, p):
        'number : LPAREN number RPAREN'
        p[0] = p[2]

##### Numbers #####
    def p_number(self, p):
        """number : function
                  | scalar
                  | complex"""
        p[0] = p[1]

    def p_scalar(self,p):
        """scalar : integer
                  | double"""
        p[0] = p[1]

    def p_integer(self, p):
        'integer : INTEGER'
        p[0] = ast.Integer(p[1])

    def p_double(self, p):
        'double : DOUBLE'
        p[0] = ast.Double(p[1])

    def p_complex(self, p):
        'complex : LPAREN number COMMA number RPAREN'
        p[0] = ast.Complex(p[2], p[4])
        
##### Functions #####
    def p_function_sin(self, p):
        'function : SIN LPAREN number RPAREN'
        p[0] = ast.Sin(p[3])

    def p_function_cos(self, p):
        'function : COS LPAREN number RPAREN'
        p[0] = ast.Cos(p[3])

    def p_function_tan(self, p):
        'function : TAN LPAREN number RPAREN'
        p[0] = ast.Tan(p[3])

    def p_function_log(self, p):
        'function : LOG LPAREN number RPAREN'
        p[0] = ast.Log(p[3])

    def p_function_exp(self, p):
        'function : EXP LPAREN number RPAREN'
        p[0] = ast.Exp(p[3])

    def p_function_sqrt(self, p):
        'function : SQRT LPAREN number RPAREN'
        p[0] = ast.Sqrt(p[3])

    def p_function_pi(self, p):
        'function : PI'
        p[0] = ast.Pi()



#Unimplemented: DEFINE_ , PRIMITIVE , OPERATION , DIRECT , ALIAS , size_rule, shape, formula, root_of_one


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

	def p_error(self, p):
		if p is not None:
			print "Line: %s Syntax error at '%s'" % (p.lineno, p.value)
		return None
