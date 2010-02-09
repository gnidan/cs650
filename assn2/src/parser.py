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
        'SUBNAME', 'DATATYPE', 'CODETYPE', 'UNROLL', 'VERBOSE', 'DEBUG', 'INTERNAL', 'OPTIMIZE',
        'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'RPAREN', 'LPAREN', 'HASH',
        'COMMA', 'COMMENT', 'INVISIBLE_COMMENT',
        'INTEGER', 'DOUBLE',
        'SIN', 'COS', 'TAN', 'LOG', 'EXP', 'SQRT', 'PI',
        'REAL', 'COMPLEX',
        'ON', 'OFF',
        'SYMBOL'
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

    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_HASH = r'\#'
    t_COMMA = r','

    def t_INVISIBLE_COMMENT(self, t):
        r';;.*'
        pass

    def t_COMMENT(self, t):
        r';.*'
        t.value = t.value[1:]
        return t

    def t_DOUBLE(self,t):
        r"""(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?""" #This is a much better decimal number
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
        t.type = self.RESERVED.get(t.value.lower(), "SYMBOL")
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
        """stmt : formula
                | directive
                | definition
                | comment
                | INVISIBLE_COMMENT"""
        p[0] = p[1]

    def p_comment(self, p):
        'comment : COMMENT'
        p[0] = ast.Comment(p[1])

    def p_directive_subname(self, p):
        'directive : HASH SUBNAME SYMBOL'
        p[0] = ast.SubName(p[3])

    def p_directive_codetype(self, p):
        'directive : HASH CODETYPE type'
        p[0] = ast.CodeType(p[3])

    def p_directive_datatype(self, p):
        'directive : HASH DATATYPE type'
        p[0] = ast.DataType(p[3])

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

    def p_type_real(self, p):
        'type : REAL'
        p[0] = ast.RealType()

    def p_type_complex(self, p):
        'type : COMPLEX'
        p[0] = ast.ComplexType()

    def p_flag_on(self, p):
        'flag : ON'
        p[0] = On(p[1])

    def p_flag_off(self, p):
        'flag : OFF'
        p[0] = Off(p[1])

    def p_definition_formula(self, p):
        'definition : LPAREN DEFINE SYMBOL formula RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_formula(self, p):
        """formula : matrix
                   | diagonal
                   | permutation
                   | rpermutation
                   | sparse
                   | compose
                   | tensor
                   | direct_sum
                   | conjugate
                   | scale
                   | f
                   | i
                   | j
                   | l
                   | o
                   | t"""
        p[0] = p[1]

    def p_formula_paren(self, p):
        'formula : LPAREN formula RPAREN'
        p[0] = p[2]

    def p_f(self, p):
        'f : LPAREN F number RPAREN'
        p[0] = ast.F(p[3])

    def p_i(self, p):
        'i : LPAREN I number RPAREN'
        p[0] = ast.I(p[3])

    def p_i2(self, p):
        'i : LPAREN I number number RPAREN'
        p[0] = ast.I(p[3], p[4])

    def p_j(self, p):
        'j : LPAREN J number RPAREN'
        p[0] = ast.J(p[3])

    def p_l(self, p):
        'l : LPAREN L number number RPAREN'
        p[0] = ast.L(p[3], p[4])

    def p_o(self, p):
        'o : LPAREN O number RPAREN'
        p[0] = ast.O(p[3])

    def p_t(self, p):
        't : LPAREN T number number RPAREN'
        p[0] = ast.T(p[3], p[4])

    def p_matrix(self, p):
        'matrix : LPAREN MATRIX matrix_row_list RPAREN'
        p[0] = p[3]

    def p_matrix_row_list(self, p):
        'matrix_row_list : matrix_row matrix_row_list'
        p[4].prepend(p[2])
        p[0] = p[4]

    def p_matrix_row_list_row(self, p):
        'matrix_row_list : matrix_row'
        p[0] = ast.Matrix()
        p[0].prepend(p[2])

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

    def p_diagonal(self, p):
        'diagonal : LPAREN DIAGONAL number_list RPAREN'
        p[0] = ast.Diagonal(p[3])

    def p_permutation(self, p):
        'permutation : LPAREN PERMUTATION number_list RPAREN'
        p[0] = ast.Permutation(p[3])

    def p_rpermutation(self, p):
        'rpermutation : LPAREN RPERMUTATION number_list RPAREN'
        p[0] = ast.RPermutation(p[3])

    def p_spare(self, p):
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

    def p_compose(self, p):
        'compose : LPAREN COMPOSE formulas RPAREN'
        p[0] = ast.Compose(p[3])

    def p_tensor(self, p):
        'tensor : LPAREN TENSOR formulas RPAREN'
        p[0] = ast.Tensor(p[3])

    def p_direct_sum(self, p):
        'direct_sum : LPAREN DIRECT_SUM formulas RPAREN'
        p[0] = ast.DirectSum(p[3])

    def p_conjugate(self, p):
        'conjugate : LPAREN CONJUGATE formula formula RPAREN'
        p[0] = ast.Conjugate(A, P)

    def p_scale(self, p):
        'scale : LPAREN SCALE number formula RPAREN'
        p[0] = ast.Scale(a, B)

    def p_formulas(self, p):
        'formulas : formula formulas'
        p[2].insert(0, p[1])
        p[0] = p[2]

    def p_formulas_end(self, p):
        'formulas : formula'
        p[0] = [ p[1] ]

    def p_definition_value(self, p):
        'definition : LPAREN DEFINE SYMBOL number RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_undefine(self, p):
        'definition : LPAREN UNDEFINE SYMBOL RPAREN'
        p[0] = ast.Undefine(p[3])

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

    def p_error(self, p):
        if p is not None:
            print "Line: %s Syntax error at '%s'" % (p.lineno, p.value)
        return None

#Unimplemented: templates, DEFINE_ , PRIMITIVE ,
#OPERATION , DIRECT , ALIAS , size_rule, shape, root_of_one
