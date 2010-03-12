#!/usr/bin/python

#SPL Symbols can be one of the following:
# PRIMITIVE      name of parameterized special matrix defined by "primitive"
#   (primitive F SPL_SHAPE_SQUARE)
#   (primitive I SPL_SHAPE_RECTDIAG)
#   (primitive O SPL_SHAPE_RECTDIAG)
#   (primitive T SPL_SHAPE_DIAG)
#   (primitive L SPL_SHAPE_SQUARE)
#   (primitive J SPL_SHAPE_SQUARE)

# OPERATION      name of matrix operation defined by "operation"
#   (operation compose    SPL_SIZE_COMPOSE)
#   (operation tensor     SPL_SIZE_TENSOR)
#   (operation direct_sum SPL_SIZE_SUM)
#   (operation conjugate  SPL_SIZE_COMPOSE)
#   (operation scale      SPL_SIZE_TENSOR)

# DIRECT    		 name of a direct matrix defined by "direct"
#   (direct matrix       SPL_SIZE_MATRIX)
#   (direct diagonal     SPL_SIZE_VECTOR)
#   (direct permutation  SPL_SIZE_VECTOR)
#   (direct rpermutation SPL_SIZE_VECTOR)
#   (direct sparse       SPL_SIZE_SPARSE)

# ALIAS     		 an alias of another symbol defined by "alias"
#   (alias comp compose)
#   (alias tens tensor)
#   (alias dsum direct_sum)
#   (alias conj conjugate)
#   (alias matx matrix)
#   (alias diag diagonal)
#   (alias perm permutation)
#   (alias rperm rpermutation)

# ICONST    		 an integer constant defined by "define"
# DCONST    		 a double constant defined by "define"
# CCONST    		 a complex constant defined by "define"
# FORMULA   		 a SPL formula defined by "define"
# CODE      		 a piece of straight-line code defined by "define_"

import numbers
import ast

class Variable:
  """Maintains the record for a particular variable in our symbol table"""
  def __init__(self):
    self.access = []

  def access(self, icode):
    """Record when a particular icode expression access this variable"""
    self.access.append(icode)

class IntegerConst(Variable):
  """Represents an Integer constant value"""
  def __init__(self, value=0):
    self.const = True
    self.value = int(value)

class RealConst(Variable):
  """Represents a Double constant value"""
  def __init__(self, value):
    self.const = True
    self.value = float(value=0)

class ComplexConst(Variable):
  """Represents a Complex constant value"""
  def __init__(self, value=0):
    self.const = True
    self.value = complex(0)

class Formula(Variable):
  """Represents a definition of a formula"""
  def __init__(self, value=None):
    self.const = False
    self.value = value

class Code(Formula):
  """Represents a definition of a formula with icode"""
  def __init__(self, value=None, icode=None):
    self.const = False
    self.value = value
    self.icode = icode

class Declaration(Variable):
  def __init__(self, size_rule, options):
    self.templates = []
    self.size_rule = size_rule
    self.options   = options

  def addTemplate(self, template):
    self.templates.insert(0, template)

  # returns true or false
  # postcondition: if true, template is filled in with wildcards assigned to
  #   matching formulas
  @staticmethod
  def compare(template, formula):
    pass

  def match(self, formula):
    for template in self.templates:
      comparison = self.compare(template, formula)

      if comparison:
        records = RecordSet()

        # setup vars for input/output and patterns
        records.x = Vector(formula.nx)
        records.y = Vector(formula.ny)

        patterns = []
        for f in template.matches:
          patterns.append( Pattern(f) )

        records.p = patterns

        return (template.icode_list, records)


class Primitive(Declaration):
  @staticmethod
  def compare(template, formula):
    if len(formula.list) != len(template.pattern.list):
      return False
    
    # p0 corresponds to the whole formula
    matches = [ formula ]

    for i in range(len(template.pattern.list)):
      t = template.pattern.list[i]
      f = formula.list[i]

      if isinstance(t, ast.Wildcard) and t == "ANY":
        matches.append(f)
      elif t != f:
        return False

    template.matches = matches
    return True
    
  def sizes_for(self, formula):
    shape = self.size_rule.lower()
    if shape == "spl_shape_square" or shape == "spl_shape_diag":
      input = formula.list[0]
      output = input
      return (output, input)
    if shape == "spl_shape_rect" or shape == "spl_shape_rectdiag":
      input = formula.list[0]
      if len(formula) > 1:
        output = formula.list[1]
      else:
        output = input
      return (output, input)

class Operation(Declaration):
  @staticmethod
  def compare(template, formula):
    if len(formula.list) != len(template.pattern.list):
      return False

    matches = [ formula ]

    for i in range(len(template.pattern.list)):
      t = template.pattern.list[i]
      f = formula.list[i]

      if isinstance(t, ast.Wildcard) and t == "ANY":
        matches.append(f)
      else:
        bool, wild = compare_trees (t, f)
        if bool:
          if wild:
            matches.append(f)
        else:
          return False

    template.matches = matches
    return True

  def compare_trees (t, f):
    if isinstance(t, ast.Wildcard) and t == "ANY":
      return (True, True)
    if isinstance(t, ast.Formula):
      if isinstance(f, ast.Formula):
        if t.symbol != f.symbol:
          return (False, False)
        if len(t.list) != len(f.list):
          return (False, False)
        wild = False
        for i in range(len(t.list)):
          mbool, mwild = compare_trees (t.list[i], f.list[i])
          if mbool == False:
            return (False, False)
          if mwild:
            wild = True
        return (True, wild)
      else:
        return (False, False)
    elif t == f:
      return (True, False)
    return (False, False)


  def sizes_for(self, formula):
    if len(formula) == 1:
      output = formula.list[0].ny
      input = formula.list[0].nx
    else:
      shape = self.size_rule.lower()
      if shape == "spl_size_ident":
        output = formula.list[0].ny
        input = formula.list[0].nx
      elif shape == "spl_size_transpose":
        output = formula.list[1].nx
        input = formula.list[0].ny
      elif shape == "spl_size_compose":
        output = formula.list[0].ny;
        input = formula.list[1].nx;
      elif shape == "spl_size_sum":
        output = formula.list[0].ny + formula.list[1].ny
        input = formula.list[0].nx + formula.list[1].nx
      elif shpae == "spl_size_tensor":
        output = formula.list[0].ny * formula.list[1].ny
        input = formula.list[0].nx * formula.list[1].nx
    return (output, input)


class Direct(Declaration):
  @staticmethod
  def compare(template, formula):
    pass

  def sizes_for(self, formula):
    pass

class Pattern(Variable):
  def __init__(self, val):
    self.val = val

class Vector(Variable):
  """Represents a vector of scalars"""
  def __init__(self, size):
    self.size = size
    self.scalars = [Variable()]*size.val #initialize vector to have a given size

class RecordSet:
  # notes: actually, maybe the behavior with setting up all the variables,
  # in particular, the i varible stack, should be behavior to put in C and
  # not at all in the compiler python code. Instead, perhaps we should just
  # be tracking usage?
  def __init__(self):
    self.__r = []
    self.__f = []
    self.__i = []
    self.__t = []

    self.realcomplex = RealConst # TODO update this
 
  def __getitem__(self, symbol):
    switch = {
        'r': lambda index, sub: self.get_r(index),
        'f': lambda index, sub: self.get_f(index),
        'i': lambda index, sub: self.get_i(index),
        'p': lambda index, sub: self.get_p(index),
        't': lambda index, sub: self.get_t(index, subscript),
        'x': lambda index, sub: self.get_x(subscript),
        'y': lambda index, sub: self.get_y(subscript)
        }
    func = switch[symbol.var_type]
    return func(symbol.index, symbol.subscript)
 
  def get_r(self, index):
    try:
      return self.__r[index]
    except IndexError as inst:
      if index == len(self.__r):
        self.__r.append(IntegerConst())
        return self.__r[index]
      else:
        raise inst
 
  def get_f(self, index):
    try:
      return self.__f[index]
    except IndexError as inst:
      if index == len(self.__f):
        self.__f.append(self.realcomplex())
        return self.__f[index]
      else:
        raise inst
 
  def append_loop(self):
    i = Int()
    self.__i.append(i)
 
  def pop_loop(self):
    self.__i.pop()
 
  def get_i(self, index):
    # i0 -> i[len(i)-1]
    index = len(self.__i) - index - 1
    return self.__i[index]
 
  def get_p(self, index):
    # pattern varible behavior is probably different in a bunch of ways
    try:
      return self.p[index]
    except IndexError as inst:
      if index == len(self.p):
        self.p.append(Pattern())
        return self.p[index]
      else:
        raise inst
 
  def new_t(self, size):
    self.__t.append(Vector(size))
    return len(self.__t) - 1
 
  def get_t(self, index, subscript=None):
    if(subscript):
      return self.__t[index][subscript]
    else:
      return self.__t[index]

  def get_x(self, subscript=None):
    if(subscript):
      return self.x[subscript]
    else:
      return self.x

  def get_y(self, subscript=None):
    if(subscript):
      return self.y[subscript]
    else:
      return self.y


class AlreadyDefinedError(Exception):
  def __init__(self, name):
    self.msg = "%s is already defined" % (name)

class SymbolTable(dict):
  """We don't really need a scope. So the symbol table is just a dictionary.
  Python keeps track of it all for us!"""
  def __setitem__(self, key, value):
    """SPL does not allow redefinitions. It must be undefined first"""
    if self.has_key(key):
      raise AlreadyDefinedError(key)
    super(SymbolTable,self).__setitem__(key, value)

  def __getitem__(self, key):
    """Get an entry from the symbol table. Returns either a constant or a list
    of ICode ops (defined values get stored as ICode, templates get matched and
    converted on way out)"""
    if isinstance(key, ast.Formula):
      declaration = self.__getitem__(key.symbol)
      return declaration.match(key)
    else:
      return super(SymbolTable,self).__getitem__(key)

  def isConst(self, key):
    if self.has_key(key):
      val = super(SymbolTable,self).__getitem__(key)
      if isinstance(val, numbers.Number):
        return True
      return val.isConst()
    raise KeyError 
