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
import re

import ply.lex as lex
import ply.yacc as yacc

import ast
import icode
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
        #self.lexer_test(data)
        return yacc.parse(data)

    def lexer_test(self,data):
        self.lexer.input(data)
        for tok in self.lexer:
            print tok.type, tok.value

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
        'DEFINE', 'UNDEFINE',
        'SUBNAME', 'DATATYPE', 'CODETYPE', 'UNROLL', 'VERBOSE', 'DEBUG', 
        'INTERNAL', 'OPTIMIZE', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 
        'RPAREN', 'LPAREN', 'HASH', 'COLON',
        'COMMA', 'COMMENT', 'INVISIBLE_COMMENT',
        'INTEGER', 'DOUBLE',
        'C', 'S', 'W', 'WR', 'WI', 'TW', 'TWR', 'TWI',
        'SIN', 'COS', 'TAN', 'LOG', 'EXP', 'SQRT', 'PI', 'WSCALAR',
        'REAL', 'COMPLEX',
        'ON', 'OFF', 'TEMPLATE', 'ANY',
        'SYMBOL', 'SHAPE', 'SIZE_RULE', 'PRIMITIVE', 'OPERATION', 'DIRECT',
        'LBRACKET', 'RBRACKET',
        'CALL', 'LOOP', 'LOOPUNROLL', 'END', 'NEWTMP', 'EQUALS',
        'ISCALAR', 'IVECTOR', 'IMATRIX'
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
        "c"            :	"C",
        "s"            :	"S",
        "tw"           :	"TW",
        "twi"          :	"TWI",
        "twr"          :	"TWR",
        "w"            :	"W",
        "wi"           :	"WI",
        "wr"           :	"WR",
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
        "direct"       :	"DIRECT",
        "div"          :	"DIV",
        "exp"          :	"EXP",
        "internal"     :	"INTERNAL",
        "log"          :	"LOG",
        "misc"         :	"MISC",
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

        "spl_shape_square"   : "SHAPE",
        "spl_shape_rect"     : "SHAPE",
        "spl_shape_diag"     : "SHAPE",
        "spl_shape_rectdiag" : "SHAPE",
        "spl_size_ident"     : "SIZE_RULE",
        "spl_size_transpose" : "SIZE_RULE",
        "spl_size_compose"   : "SIZE_RULE",
        "spl_size_sum"       : "SIZE_RULE",
        "spl_size_tensor"    : "SIZE_RULE",
        "spl_size_matrix"    : "SIZE_RULE",
        "spl_size_vector"    : "SIZE_RULE",
        "spl_size_sparse"    : "SIZE_RULE",

        "newtmp"       :	"NEWTMP",
        "deftemp"       :	"NEWTMP",
        "do"           :	"LOOP",
        "dounroll"     :	"LOOPUNROLL",
        "end"          :	"END",
    }

    t_EQUALS = r'='
    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_MOD = r'%'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
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
        t.type = self.RESERVED.get(t.value.lower(), "SYMBOL")
        return t
    
    def t_IMATRIX(self, t):
        r'\$p\d+\.a'
        exp = re.compile(r'\$(?P<Type>.)(?P<Index>.*)')
        match = exp.match(t.value)
        if not match:
          raise Exception()
        type, index = match.group('Type','Index')
        if(index):
          t.value = (type, index)
        else:
          t.value = (type, 0)
        return t

    def t_IVECTOR(self, t):
        r'\$(x|y|t\d+)'
        exp = re.compile(r'\$(?P<Type>.)(?P<Index>.*)')
        match = exp.match(t.value)
        if not match:
          raise Exception()
        type, index = match.group('Type','Index')
        if(index):
          t.value = (type, index)
        else:
          t.value = (type, 0)
        return t

    def t_ISCALAR(self, t):
        r'\$([rfi]\d+|p\d+(\.(nx|ny|nx_1|ny_1|matrix_row|matrix_col))?)'
        exp = re.compile(r'\$(?P<Type>.)(?P<Index>.+)')
        match = exp.match(t.value)
        if not match:
          raise Exception()
        type, index = match.group('Type','Index')
        t.value = (type, index)
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
                | symbol
                | comment 
                | directive
                | definition
                | declaration
                | template"""
        p[0] = p[1]

    def p_symbol(self, p):
        'symbol : SYMBOL'
        p[0] = ast.Symbol(p[1])

##### Formulas #####

    def p_formula_sexp(self, p):
        'formula : LPAREN symbol values RPAREN'
        p[0] = ast.Formula(p[2], p[3])

    def p_formula_stride(self, p):
        'formula : LPAREN symbol values COMMA stride RPAREN'
        p[0] = ast.Formula(p[2], p[3], stride=p[5])

    def p_stride(self, p):
        'stride : value COLON value COLON value'
        p[0] = (p[1], p[3], p[5])

    def p_value(self, p):
      """value : formula
               | expression
               | symbol
               | vector
               | wildcard"""
      p[0] = p[1]

    def p_wildcard(self, p):
        'wildcard : ANY'
        p[0] = ast.Wildcard(p[1])

    def p_vector(self, p):
        'vector : LPAREN values RPAREN'
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
    def p_directive(self, p):
        """directive : HASH SUBNAME symbol
                     | HASH CODETYPE type
                     | HASH DATATYPE type
                     | HASH OPTIMIZE flag
                     | HASH UNROLL flag
                     | HASH VERBOSE flag
                     | HASH INTERNAL flag
                     | HASH DEBUG flag"""
        p[0] = self.create_or_get(p[2], ast.Directive)(p[3]) 

    ##    types
    def p_type_real(self, p):
        'type : REAL'
        p[0] = numbers.Real

    def p_type_complex(self, p):
        'type : COMPLEX'
        p[0] = numbers.Complex

    ##    flags
    def p_flag_on(self, p):
        'flag : ON'
        p[0] = True

    def p_flag_off(self, p):
        'flag : OFF'
        p[0] = False

##### Assignments #####

    ##    define Symbol / define Value
    def p_definition_formula(self, p):
        'definition : LPAREN DEFINE symbol formula RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_definition_value(self, p):
        'definition : LPAREN DEFINE symbol number RPAREN'
        p[0] = ast.Define(p[3], p[4])

    def p_undefine(self, p):
        'definition : LPAREN UNDEFINE symbol RPAREN'
        p[0] = ast.Undefine(p[3])


##### Templates #####

    ##    template
    def p_template_formula(self, p):
        'template : LPAREN TEMPLATE formula LPAREN icode_program RPAREN RPAREN'
        p[0] = ast.Template(p[3], p[5])

    ##    declarations
    def p_primitive(self, p):
        'declaration : LPAREN PRIMITIVE symbol SHAPE RPAREN'
        p[0] = ast.Primitive(p[3], p[4])

    def p_operation(self, p):
        'declaration : LPAREN OPERATION symbol SIZE_RULE RPAREN'
        p[0] = ast.Operation(p[3], p[4])

    def p_direct(self, p):
        'declaration : LPAREN DIRECT symbol SIZE_RULE RPAREN'
        p[0] = ast.Direct(p[3], p[4])
    def p_number_neg(self, p):
        'number : MINUS number %prec UMINUS'
        p[0] = ast.Operator(p[2], 'neg')

    def p_number_paren(self, p):
        'number : LPAREN number RPAREN'
        p[0] = p[2]

##### Expressions and Numbers #####
    def p_expression_number(self, p):
        """expression : number
                      | symbol"""
        p[0] = p[1]

    def p_number(self, p):
        """number : scalar
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
        'complex : LPAREN expression COMMA expression RPAREN'
        p[0] = ast.Complex(p[2], p[4])

    def p_expression(self, p):
        """expression : expression PLUS expression
                      | expression MINUS expression
                      | expression MULT expression
                      | expression DIV expression
                      | expression MOD expression"""
        p[0] = ast.Operator(p[1], self.binop_alias[p[2]], p[3])

    def p_expression_neg(self, p):
        'expression : MINUS expression %prec UMINUS' 
        p[0] = ast.Neg(p[2])

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
        'i_W : W LPAREN ivalue ivalue RPAREN'
        p[0] = ast.W(p[3], p[4])

    def p_WR(self, p):
        'i_WR : WR LPAREN ivalue ivalue RPAREN'
        p[0] = ast.WR(p[3], p[4])

    def p_WI(self, p):
        'i_WI : WI LPAREN ivalue ivalue RPAREN'
        p[0] = ast.WI(p[3], p[4])

    def p_TW(self, p):
        'i_TW : TW LPAREN ivalue ivalue ivalue RPAREN'
        p[0] = ast.TW(p[3], p[4], p[5])

    def p_TWR(self, p):
        'i_TWR : TWR LPAREN ivalue ivalue ivalue RPAREN'
        p[0] = ast.TWR(p[3], p[4], p[5])

    def p_TWI(self, p):
        'i_TWI : TWI LPAREN ivalue ivalue ivalue RPAREN'
        p[0] = ast.TWI(p[3], p[4], p[5])

    def p_C(self, p):
        'i_C : C LPAREN ivalue ivalue RPAREN'
        p[0] = ast.C(p[3], p[4])

    def p_S(self, p):
        'i_S : S LPAREN ivalue ivalue RPAREN'
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
        'function : function_name LPAREN ivalue RPAREN'
        p[0] = self.create_or_get(p[1], ast.Function)(p[3])

    def p_function_pi(self, p):
        'function : PI'
        p[0] = ast.Pi()

    def p_function_w(self, p):
        'function : WSCALAR LPAREN ivalue RPAREN'
        p[0] = ast.w(p[3])

    def p_function_w_exp(self, p):
        'function : WSCALAR LPAREN ivalue COMMA ivalue RPAREN'
        p[0] = ast.w(p[3], p[5])

    def p_error(self, p):
        if p is not None:
          print "Line %d: Syntax error at '%s'" % (p.lineno, p.value)
        return None

##### ICode #####
    def p_icode_program(self, p):
        'icode_program : icode_list'
        p[0] = p[1]

    def p_icode_list(self, p):
        'icode_list : icode icode_list'
        p[2].prepend(p[1])
        p[0] = p[2]

    def p_icode_list_end(self, p):
        'icode_list : icode'
        p[0] = icode.StmtList(p[1])

    def p_icode(self, p):
        """icode : add
                 | sub
                 | mul
                 | div
                 | mod
                 | assn
                 | call
                 | do
                 | dounroll
                 | end
                 | newtmp
                 | comment"""
        p[0] = p[1]

    def p_ivalue(self, p):
        """ivalue : double
                  | integer
                  | ivar
                  | intrinsic
                  | function"""
        p[0] = p[1]

    def p_ivar_scalar(self, p):
        'ivar : ISCALAR'
        p[0] = icode.Symbol(p[1])

    def p_ivar_vector(self, p):
        'ivar : IVECTOR LPAREN subscript RPAREN'
        p[0] = icode.Symbol(p[1], subscript=p[3])

    def p_ivar_matrix(self, p):
        'ivar : IMATRIX LPAREN ivalue ivalue RPAREN'
        p[0] = icode.Symbol(p[1], subscript=(p[3], p[4]))

    def p_subscript_simple(self, p):
        'subscript : index'
        p[0] = icode.Subscript(p[1])

    def p_subscript_multiplicands(self, p):
        'subscript : index multiplicands'
        p[0] = icode.Subscript(p[1], *p[2])

    def p_multiplicands(self, p):
        'multiplicands : ivalue multiplicands'
        p[2].insert(0, p[1])
        p[0] = p[2]

    def p_multiplicands_end(self, p):
        'multiplicands : ivalue'
        p[0] = [ p[1] ]

    def p_index_simple(self, p):
        'index : ivalue'
        p[0] = icode.Index(p[1])

    def p_index_range(self, p):
        'index : ivalue COLON ivalue COLON ivalue'
        p[0] = icode.Range(p[1], p[3], p[5])

    def p_add(self, p):
        'add : ivar EQUALS ivalue PLUS ivalue'
        p[0] = icode.Add(p[1], p[3], p[5])

    def p_sub(self, p):
        'sub : ivar EQUALS ivalue MINUS ivalue'
        p[0] = icode.Sub(p[1], p[3], p[5])

    def p_mul(self, p):
        'mul : ivar EQUALS ivalue MULT ivalue'
        p[0] = icode.Mul(p[1], p[3], p[5])

    def p_div(self, p):
        'div : ivar EQUALS ivalue DIV ivalue'
        p[0] = icode.Div(p[1], p[3], p[5])

    def p_mod(self, p):
        'mod : ivar EQUALS ivalue MOD ivalue'
        p[0] = icode.Mod(p[1], p[3], p[5])

    def p_assn(self, p):
        'assn : ivar EQUALS ivalue'
        p[0] = icode.Copy(p[1], p[3])
      
    def p_call(self, p):
        'call : ivar EQUALS CALL symbol'
        p[0] = icode.Call(p[1], p[4])

    def p_call_arg(self, p):
        'call : ivar EQUALS CALL symbol ivar'
        p[0] = icode.Call(p[1], p[4], p[5])

    def p_do(self, p):
        'do : LOOP ivalue'
        p[0] = icode.Do(p[2])

    def p_dounroll(self, p):
        'dounroll : LOOPUNROLL ivalue'
        p[0] = icode.DoUnroll(p[2])

    def p_do_end(self, p):
      """end : END LOOP
             | END LOOPUNROLL
             | END"""
      p[0] = icode.End()

    def p_newtmp(self, p):
        'newtmp : NEWTMP ivalue'
        p[0] = icode.DefTmp(p[2])

#Unimplemented: DEFINE_ ALIAS
#               size_rule shape root_of_one
