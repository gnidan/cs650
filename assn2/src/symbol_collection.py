#!/usr/bin/python

class Variable:
  """Maintains the record for a particular variable in our symbol table"""

  def __init__(self):
    self.access = []

  def access(self, icode):
    """Record when a particular icode expression access this variable"""
    self.access.append(icode)

class Scalar(Variable):
  """Represents a scalar value"""
  pass

class Int(Scalar):
  def __init__(self):
    self.value = 0

class RealComplex(Scalar):
  def __init__(self):
    self.value = 0

class Pattern(Variable):
  def __init__(self):
    self.Value = None     # TODO fill this in later for struct

class Vector(Variable):
  """Represents a vector of scalars"""
  def __init__(self, size):
    self.size = size
    self.scalars = [Scalar()] * size #initialize vector to have a given size

class SymbolCollection:
  def __init__(self, input_size, output_size):
    self.r       = []
    self.f       = []
    self.i       = []
    self.p       = []
    self.t       = []
    self.x       = Vector(input_size)
    self.y       = Vector(output_size)
    self.sym_tab = SymbolTable()

  def new_r(self):
    r = Int()
    self.r.append(r)
    return r

  def new_f(self):
    f = RealComplex()
    self.f.append(f)
    return f

  def new_i(self):
    i = Int()
    self.i.append(i)
    return i

  def new_p(self):
    p = new Pattern()
    self.p.append(p)
    return p

  def new_t(self, size):
    t = new Vector(size)
    self.t.append(t)
    return t

class SymbolTable:
  def __init__(self):
    dict = {} # TODO redefine this to be set to the dict containing all
              # the predefined values
    self.depth = 0
    self.table = [dict]

  def __getitem__(self, key):
    dict = self.table[self.depth]
    return dict[key]

  def __setitem__(self, key, value):
    dict = self.table[self.depth]
    dict[name] = value

  def __delitem__(self, key):
    dict = self.table[self.depth]
    del dict[name]

  def append_scope(self):
    dict = self.table[self.depth]
    self.table.append(dict.copy())
    depth += 1

  def pop_scope(self):
    self.table.pop()
    depth -= 1
