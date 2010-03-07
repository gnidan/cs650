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
  def __init__(self, size_rule):
    templates = []
    self.size_rule = size_rule;

  def addTemplate(self, template):
    self.templates.insert(0, Template(icode_list=template.icode_list, 
      pattern=template.pattern, condition=template.condition))

class Primitive(Declaration):
  pass

class Operation(Declaration):
  pass

class Direct(Declaration):
  pass

class Template:
  def __init__(self, icode_list, pattern, condition=None):
    self.icode_list = icode_list
    self.pattern = pattern
    self.condition = condition

class Pattern(Variable):
  def __init__(self):
    self.Value = None     # TODO fill this in later for struct

class Vector(Variable):
  """Represents a vector of scalars"""
  def __init__(self, size):
    self.size = size
    self.scalars = [Scalar()] * size #initialize vector to have a given size

class SymbolCollection:
  # notes: actually, maybe the behavior with setting up all the variables,
  #   in particular, the i varible stack, should be behavior to put in C and
  #   not at all in the compiler python code. Instead, perhaps we should just
  #   be tracking usage?
  def __init__(self, input_size, output_size):
    self.r       = []
    self.f       = []
    self.i       = []
    self.p       = []
    self.t       = []
    self.x       = Vector(input_size)
    self.y       = Vector(output_size)
    self.sym_tab = SymbolTable()

  def r(self, index):
    try:
      return self.r[index]
    except IndexError as inst:
      if index == len(self.r):
        self.r.append(Int())
        return self.r[index]
      else:
        raise inst

  def f(self, index):
    try:
      return self.f[index]
    except IndexError as inst:
      if index == len(self.f):
        self.f.append(RealComplex())
        return self.f[index]
      else:
        raise inst

  def append_loop(self):
    i = Int()
    self.i.append(i)

  def pop_loop(self):
    self.i.pop()

  def i(self, index):
    # i0 -> i[len(i)-1]
    index = len(self.i) - index - 1
    return self.i[index]

  def p(self, index):
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
    self.t.append(Vector(size))
    return len(self.t) - 1

  def t(self, index, subscript=None):
    if(subscript):
      return self.t[index][subscript]
    else:
      return self.t[index]




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

  def isConst(self, key):
    if self.has_key(key):
      val = super(SymbolTable,self).__getitem__(key)
      if isinstance(val, numbers.Number):
        return True
      return val.isConst()
    raise KeyError
