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

import symbols
import numbers
import ast

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
 
  def __getitem__(self, symbol):
    switch = {
        'r': lambda symbol: self.get_r(symbol.index),
        'f': lambda symbol: self.get_f(symbol.index),
        'i': lambda symbol: symbols.IRef(symbol.index),
        'p': lambda symbol: self.get_p(symbol),
        't': lambda symbol: self.get_t(symbol.index, sub),
        'x': lambda symbol: self.get_x(symbol.sub),
        'y': lambda symbol: self.get_y(symbol.sub)
        }
    func = switch[symbol.var_type]
    return func(symbol)
 
  def get_r(self, index):
    try:
      return self.__r[index]
    except IndexError as inst:
      if index == len(self.__r):
        self.__r.append(symbols.VarR())
        return self.__r[index]
      else:
        raise inst
 
  def get_f(self, index):
    try:
      return self.__f[index]
    except IndexError as inst:
      if index == len(self.__f):
        self.__f.append(symbols.VarF())
        return self.__f[index]
      else:
        raise inst
 
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
    self.__t.append(symbols.Vec(size))
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
