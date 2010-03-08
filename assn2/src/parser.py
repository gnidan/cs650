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
import numbers

class SPLParser:
    def __init__(self,debug=False):
        self.debug = debug
        modname = self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_parsetab"
        self.types = {}

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

    def create_or_get(self, name, subclass=object):
        if name not in self.types:
            self.types[name] = type(name, (subclass,), {})
        return self.types[name]

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
        'SUBNAME', 'DATATYPE', 'CODETYPE', 'UNROLL', 'VERBOSE', 'DEBUG', 'INTERNAL', 'OPTIMIZE',
        'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'RPAREN', 'LPAREN', 'HASH', 'COLON',
        'COMMA', 'COMMENT', 'INVISIBLE_COMMENT',
        'INTEGER', 'DOUBLE',
        'C', 'S', 'W', 'WR', 'WI', 'TW', 'TWR', 'TWI',
        'SIN', 'COS', 'TAN', 'LOG', 'EXP', 'SQRT', 'PI', 'WSCALAR',
        'REAL', 'COMPLEX',
        'ON', 'OFF',
        'SYMBOL'
    )

    binop_alias = {
        '+'  : 'add',
        '-' : 'sub',
        '*'  : 'mul',
        '/'   : 'div',
        '%'   : 'mod',
        }

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
        "any"          :	"ANYNODE",
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
        "w"            :	"WSCALAR",
        "F"            : "F",
        "I"            : "I",
        "J"            : "J",
        "L"            : "L",
        "O"            : "O",
        "T"            : "T",
        "direct_sum"   :	"DIRECT_SUM",
        "compose"      :  "COMPOSE",
        "tensor"       :  "TENSOR",
        "matrix"       :  "MATRIX",
        "permutation"  :  "PERMUTATION",
        "rpermutation" :  "RPERMUTATION",
        "diagonal"     :  "DIAGONAL",
    }

    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_HASH = r'\#'
    t_COMMA = r','
    t_COLON = r':'

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
        """stmt : definition
                | formula
                | directive
                | comment
                | INVISIBLE_COMMENT"""
        p[0] = p[1]

    def p_directive(self, p):
        """directive : HASH SUBNAME SYMBOL
                     | HASH CODETYPE type
                     | HASH DATATYPE type
                     | HASH OPTIMIZE flag
                     | HASH UNROLL flag
                     | HASH VERBOSE flag
                     | HASH INTERNAL flag
                     | HASH DEBUG flag"""
        p[0] = self.create_or_get(p[2], ast.Directive)(p[3])

    def p_type_real(self, p):
        'type : REAL'
        p[0] = numbers.Real

    def p_type_complex(self, p):
        'type : COMPLEX'
        p[0] = numbers.Complex

    def p_flag_on(self, p):
        'flag : ON'
        p[0] = True

    def p_flag_off(self, p):
        'flag : OFF'
        p[0] = False

    def p_comment(self, p):
        'comment : COMMENT'
        p[0] = ast.Comment(p[1])

    def p_definition_formula(self, p):
        'definition : LPAREN DEFINE SYMBOL formula RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_formula(self, p):
        """formula : constructor
                   | matrix
                   | sparse
                   | operation
                   | scale
                   | param_matrix"""
#                   | t"""
        p[0] = p[1]

    def p_formula_symbol(self, p):
        'formula : SYMBOL'
        p[0] = ast.Symbol(p[1])

    def p_formula_paren(self, p):
        'formula : LPAREN formula RPAREN'
        p[0] = p[2]

    #TODO should add SCALE
    def p_operation_name(self, p):
        """operation_name : COMPOSE
                          | TENSOR
                          | DIRECT_SUM
                          | CONJUGATE"""
        p[0] = p[1]

    #TODO should add MATRIX and SPARSE
    def p_constructor_name(self, p):
        """constructor_name : DIAGONAL
                            | PERMUTATION
                            | RPERMUTATION"""
        p[0] = p[1]

    #TODO should include T
    def p_param_matrix_name(self, p):
        """param_matrix_name : F
                             | I
                             | J
                             | L
                             | O
                             | T"""
        p[0] = p[1]

    def p_constructor(self, p):
        'constructor : LPAREN constructor_name number_list RPAREN'
        p[0] = self.create_or_get(p[2], ast.Formula)(p[3])

    def p_operation(self, p):
        'operation : LPAREN operation_name formulas RPAREN'
        p[0] = self.create_or_get(p[2], ast.Formula)(p[3])

    def p_param_matrix(self, p):
        """param_matrix : LPAREN param_matrix_name nums RPAREN"""
        p[0] = self.create_or_get(p[2], ast.Formula)(p[3])

    def p_scale(self, p):
        'scale : LPAREN SCALE number formula RPAREN'
        p[0] = ast.Scale(a, B)

    # def p_index(self, p):
    #     'index : number COLON number COLON number'
    #     p[0] = ast.Index(p[1], p[3], p[5])

    #TODO ELIMINATE!
    # def p_t(self, p):
    #     't : LPAREN T number number RPAREN'
    #     p[0] = ast.T(p[3], p[4])

    # def p_t_idx(self, p):
    #     't : LPAREN T number number COMMA index RPAREN'
    #     p[0] = ast.T(p[3], p[4], p[6])

    def p_matrix(self, p):
        'matrix : LPAREN MATRIX matrix_row_list RPAREN'
        p[0] = p[3]

    def p_matrix_row_list(self, p):
        'matrix_row_list : matrix_row matrix_row_list'
        p[2].prepend(p[1])
        p[0] = p[2]

    def p_matrix_row_list_row(self, p):
        'matrix_row_list : matrix_row'
        p[0] = ast.Matrix()
        p[0].prepend(p[1])

    def p_matrix_row(self, p):
        'matrix_row : number_list'
        p[0] = ast.MatrixRow(p[1])

    def p_number_list(self, p):
        'number_list : LPAREN nums RPAREN'
        p[0] = p[2]

    def p_numbers(self, p):
        'nums : number nums'
        p[2].insert(0, p[1])
        p[0] = p[2]

    def p_numbers_end(self, p):
        'nums : number'
        p[0] = [p[1]]

    def p_formulas(self, p):
        'formulas : formula formulas'
        p[2].insert(0, p[1])
        p[0] = p[2]

    def p_formulas_end(self, p):
        'formulas : formula'
        p[0] = [ p[1] ]

    def p_sparse(self, p):
        'sparse : LPAREN SPARSE triple_list RPAREN'
        p[0] = ast.Sparse(p[3])

    def p_triple_list(self, p):
        'triple_list : triple triple_list'
        p[2].insert(0, p[1])
        p[0] = p[1]

    def p_triple_list_end(self, p):
        'triple_list : triple'
        p[0] = [ p[1] ]

    def p_triple(self, p):
        'triple : LPAREN number number number RPAREN'
        p[0] = ast.SparseElement(p[2], p[3], p[4])

    def p_definition_value(self, p):
        'definition : LPAREN DEFINE SYMBOL number RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_undefine(self, p):
        'definition : LPAREN UNDEFINE SYMBOL RPAREN'
        p[0] = ast.Undefine(p[3])

##### Operators #####
    def p_bin_op(self, p):
        """number : number PLUS number
                  | number MINUS number
                  | number MULT number
                  | number DIV number
                  | number MOD number"""
        p[0] = ast.Operator(p[1], self.binop_alias[p[2]], p[3])

    def p_number_neg(self, p):
        'number : MINUS number %prec UMINUS'
        p[0] = ast.Operator(p[2], 'neg')

    def p_number_paren(self, p):
        'number : LPAREN number RPAREN'
        p[0] = p[2]

##### Numbers #####
    def p_number(self, p):
        """number : function
                  | scalar
                  | complex
                  | intrinsic"""
        p[0] = p[1]

    def p_number_symbol(self, p):
        'number : SYMBOL'
        p[0] = ast.Symbol(p[1])

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

##### Functions #####
    def p_function_name(self, p):
        """function_name : SIN
                         | COS
                         | TAN
                         | LOG
                         | EXP
                         | SQRT"""
        p[0] = p[1]

    def p_function_sin(self, p):
        'function : function_name LPAREN number RPAREN'
        p[0] = self.create_or_get(p[1], ast.Function)(p[3])

    def p_function_pi(self, p):
        'function : PI'
        p[0] = ast.Pi()

    def p_function_w(self, p):
        'function : WSCALAR LPAREN number RPAREN'
        p[0] = ast.w(p[3])

    def p_function_w_exp(self, p):
        'function : WSCALAR LPAREN number COMMA number RPAREN'
        p[0] = ast.w(p[3], p[5])

    def p_error(self, p):
        if p is not None:
            print "Line: %s Syntax error at '%s'" % (p.lineno, p.value)
        return None

#Unimplemented: templates DEFINE_ PRIMITIVE OPERATION DIRECT ALIAS
#               size_rule shape root_of_one
