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

class SPLParser:
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
#        self.lexer_test(data)
        return yacc.parse(data)

    def lexer_test(self,data):
        self.lexer.input(data)
        for tok in self.lexer:
            print tok.type, tok.value

    ##### LEX #################################################################

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIV', 'MOD'),
#        ('right','UMINUS')
    )

    # List of token names.	 This is always required
    tokens = (
        'DEFINE', 'UNDEFINE',
        'SUBNAME', 'DATATYPE', 'CODETYPE', 'UNROLL', 'VERBOSE', 'DEBUG', 
        'INTERNAL', 'OPTIMIZE', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 
        'RPAREN', 'LPAREN', 'HASH', #'COLON',
#        'LBRACKET', 'RBRACKET',
        'COMMA', 'COMMENT', 'INVISIBLE_COMMENT',
        'INTEGER', 'DOUBLE',
        'C', 'S', 'W', 'WR', 'WI', 'TW', 'TWR', 'TWI',
        'SIN', 'COS', 'TAN', 'LOG', 'EXP', 'SQRT', 'PI', 'WSCALAR',
        'REAL', 'COMPLEX',
        'ON', 'OFF', 'TEMPLATE', 'ANY',
        'SYMBOL'
    )

    # dictionary of reserved words
    RESERVED = {
        "C"            :	"C",
        "S"            :	"S",
        "TW"           :	"TW",
        "TWI"          :	"TWI",
        "TWR"          :	"TWR",
        "W"            :	"W",
        "WI"           :	"WI",
        "WR"           :	"WR",
        "alias"        :	"ALIAS",
        "any"          :	"ANY",
        "call"         :	"CALL",
        "codetype"     :	"CODETYPE",
        "complex"      :	"COMPLEX",
        "cos"          :	"COS",
        "datatype"     :	"DATATYPE",
        "debug"        :	"DEBUG",
        "def"          :	"DEFINE",
        "define"       :	"DEFINE",
        "define_"      :	"DEFINE_",
        "deftemp"      :	"DEFTEMP",
        "direct"       :	"DIRECT",
        "div"          :	"DIV",
        "do"           :	"LOOP",
        "dounroll"     :	"LOOPUNROLL",
        "end"          :	"LOOPEND",
        "exp"          :	"EXP",
        "internal"     :	"INTERNAL",
        "log"          :	"LOG",
        "misc"         :	"MISC",
        "mod"          :	"MOD",
        "off"          :	"OFF",
        "on"           :	"ON",
        "operation"    :	"OPERATION",
        "optimize"     :	"OPTIMIZE",
        "pi"           :	"PI",
        "primitive"    :	"PRIMITIVE",
        "real"         :	"REAL",
        "recursive"    :	"RECURSIVE",
        "slef"         :	"SELFNODE",
        "sin"          :	"SIN",
        "sqrt"         :	"SQRT",
        "subname"      :	"SUBNAME",
        "tan"          :	"TAN",
        "template"     :	"TEMPLATE",
        "undef"        :	"UNDEFINE",
        "undefine"     :	"UNDEFINE",
        "unroll"       :	"UNROLL",
        "verbose"      :	"VERBOSE",
    }

    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_MULT = r'\*'
    t_DIV = r'/'
#    t_LBRACKET = r'\['
#    t_RBRACKET = r'\]'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_HASH = r'\#'
    t_COMMA = r','
#    t_COLON = r':'

    t_WSCALAR = r'w'

    def t_INVISIBLE_COMMENT(self, t):
        r';;.*'
        pass

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

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
        return t
        #t.lexer.skip(1)

    ##### YACC ################################################################

##### Structure of Program #####

    def p_program(self, p):
        'program : stmt_list'
        p[0] = ast.Program(p[1])

    def p_stmt_list(self, p):
        'stmt_list : stmt stmt_list'
        p[2].prepend(p[1])
        p[0] = p[2]

    def p_stmt_list_tail(self, p):
        'stmt_list : stmt'
        p[0] = ast.StmtList(p[1])

    def p_stmt(self, p):
        """stmt : formula 
                | comment 
                | directive
                | definition
                | template"""
        print p[1]
        p[0] = p[1]

##### Formulas #####

    def p_formula_sexp(self, p):
        'formula : LPAREN SYMBOL values RPAREN'
        p[0] = ast.Formula(p[3], *p[4])

    def p_formula_anynode(self, p):
        'formula : ANY'
        if self.TEMPLATE_MODE == False:
          raise Exception("Wildcard not allowed except in template")
        p[0] = ast.Wildcard(p[1])

    def p_value(self, p):
      """value : formula
               | number"""
      p[0] = p[1]
            

    def p_values(self, p):
        'values : value values'
        p[2].insert(0,p[1])
        p[0] = p[2]

    def p_values_end(self, p):
        'values : value'
        p[0] = [ p[1] ]

##### Comments #####

    def p_comment(self, p):
        'comment : COMMENT'
        p[0] = ast.Comment(p[1])

    def p_invisible_comment(self, p):
        'comment : INVISIBLE_COMMENT'

##### Directives #####

    ##    #subname
    def p_directive_subname(self, p):
        'directive : HASH SUBNAME SYMBOL'
        p[0] = ast.SubName(ast.Name(p[3]))

    ##    #codetype / #datatype
    def p_directive_codetype(self, p):
        'directive : HASH CODETYPE type'
        p[0] = ast.CodeType(p[3])

    def p_directive_datatype(self, p):
        'directive : HASH DATATYPE type'
        p[0] = ast.DataType(p[3])

    ##    types
    def p_type_real(self, p):
        'type : REAL'
        p[0] = ast.RealType()

    def p_type_complex(self, p):
        'type : COMPLEX'
        p[0] = ast.ComplexType()

    ##    #optimize / #unroll
    def p_directive_optimize(self, p):
        'directive : HASH OPTIMIZE flag'
        p[0] = ast.Optimize(p[3])

    def p_directive_unroll(self, p):
        'directive : HASH UNROLL flag'
        p[0] = ast.Unroll(p[3])

    ##    #debug / #verbose / #internal
    def p_directive_debug(self, p):
        'directive : HASH DEBUG flag'
        p[0] = ast.Debug(p[3])

    def p_directive_verbose(self, p):
        'directive : HASH VERBOSE flag'
        p[0] = ast.Verbose(p[3])

    def p_directive_internal(self, p):
        'directive : HASH INTERNAL flag'
        p[0] = ast.Internal(p[3])

    ##    flags
    def p_flag_on(self, p):
        'flag : ON'
        p[0] = ast.On()

    def p_flag_off(self, p):
        'flag : OFF'
        p[0] = ast.Off()

##### Assignments #####

    ##    define Symbol / define Value
    def p_definition_formula(self, p):
        'definition : LPAREN DEFINE SYMBOL formula RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_definition_value(self, p):
        'definition : LPAREN DEFINE SYMBOL number RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_undefine(self, p):
        'definition : LPAREN UNDEFINE SYMBOL RPAREN'
        p[0] = ast.Undefine(p[3])

#    def p_template_formula_condition(self, p):
#        'template : LPAREN TEMPLATE LBRACKET condition RBRACKET pattern 
#            icode_list RPAREN'
#        p[0] = ast.Template(p[6], p[7], p[4])

##### Templates #####

    ##    template
    def p_template_formula(self, p):
        'template : LPAREN TEMPLATE formula RPAREN'
        self.TEMPLATE_MODE = True
        p[0] = ast.Template(p[3], p[4])
        self.TEMPLATE_MODE = False

##### Numbers #####

    def p_number(self, p):
        """number : scalar
                  | complex
                  | expression
                  | intrinsic
                  | function"""
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

    def p_expression_add(self, p):
        'expression : number PLUS number'
        p[0] = ast.Add(p[1], p[3])

    def p_expression_sub(self, p):
        'expression : number MINUS number'
        p[0] = ast.Sub(p[1], p[3])

    def p_expression_mul(self, p):
        'expression : number MULT number'
        p[0] = ast.Mul(p[1], p[3])

    def p_expression_div(self, p):
        'expression : number DIV number'
        p[0] = ast.Div(p[1], p[3])

    def p_expression_mod(self, p):
        'expression : number MOD number'
        p[0] = ast.Div(p[1], p[3])

#    def p_expression_neg(self, p):
#        'expression : MINUS number %prec UMINUS' 
#        p[0] = ast.Neg(p[2])

    def p_expression_paren(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

##### Intrinsics and Functions #####

    def p_intrinsic(self, p):
        """intrinsic : i_W
                     | i_WR
                     | i_WI
                     | i_TW
                     | i_TWR
                     | i_TWI
                     | i_C
                     | i_S"""
        p[0] = p[1]

    def p_W(self, p):
        'i_W : W LPAREN number number RPAREN'
        p[0] = ast.W(p[3], p[4])

    def p_WR(self, p):
        'i_WR : WR LPAREN number number RPAREN'
        p[0] = ast.WR(p[3], p[4])

    def p_WI(self, p):
        'i_WI : WI LPAREN number number RPAREN'
        p[0] = ast.WI(p[3], p[4])

    def p_TW(self, p):
        'i_TW : TW LPAREN number number number RPAREN'
        p[0] = ast.TW(p[3], p[4], p[5])

    def p_TWR(self, p):
        'i_TWR : TWR LPAREN number number number RPAREN'
        p[0] = ast.TWR(p[3], p[4], p[5])

    def p_TWI(self, p):
        'i_TWI : TWI LPAREN number number number RPAREN'
        p[0] = ast.TWI(p[3], p[4], p[5])

    def p_C(self, p):
        'i_C : C LPAREN number number RPAREN'
        p[0] = ast.C(p[3], p[4])

    def p_S(self, p):
        'i_S : S LPAREN number number RPAREN'
        p[0] = ast.S(p[3], p[4])

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

    def p_function_w(self, p):
        'function : WSCALAR LPAREN number RPAREN'
        p[0] = ast.w(p[3])

    def p_function_w2(self, p):
        'function : WSCALAR LPAREN number COMMA number RPAREN'
        p[0] = ast.w(p[3], p[5])

    def p_error(self, p):
        if p is not None:
            print "Line: %s Syntax error at '%s'" % (p.lineno, p.value)
        return None

#Unimplemented: templates DEFINE_ PRIMITIVE OPERATION DIRECT ALIAS
#               size_rule shape root_of_one
