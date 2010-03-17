#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

symbols.py Contains all of the variable types referenced at various stages of ICode.
"""

import numbers
import ast

class RecordSet:
  # notes: actually, maybe the behavior with setting up all the variables,
  # in particular, the i varible stack, should be behavior to put in C and
  # not at all in the compiler python code. Instead, perhaps we should just
  # be tracking usage?
  def __init__(self):
    self.rs = {}
    self.fs = {}
    self.ts = []
 
  def __getitem__(self, symbol):
    switch = {
        'r': lambda symbol: self.rs.setdefault(symbol.index, VarR()),
        'f': lambda symbol: self.fs.setdefault(symbol.index, VarF()),
        'i': lambda symbol: IRef(symbol.index),
        'p': lambda symbol: self.get_p(symbol.index, symbol.subscript),
        't': lambda symbol: self.get_t(symbol.index, subscript),
        'x': lambda symbol: self.get_x(symbol.subscript),
        'y': lambda symbol: self.get_y(symbol.subscript)
        }
    func = switch[symbol.var_type]
    return func(symbol)
 
  def get_p(self, index, subscript):
    if subscript:
      return Index(self.ps[index], subscript)
    else:
      return self.ps[index]
 
  def new_t(self, size):
    self.ts.append(Vec(size))
    return len(self.ts) - 1
 
  def get_t(self, index, subscript=None):
    if(subscript):
      return Index(self.ts[index], subscript)
    else:
      return self.ts[index]

  def get_x(self, subscript=None):
    if(subscript):
      return Index(self.x, subscript)
    else:
      return self.x

  def get_y(self, subscript=None):
    if(subscript):
      return Index(self.y, subscript)
    else:
      return self.y

class Declaration:
  def __init__(self, size_rule):
    self.templates = []
    self.size_rule = size_rule
 
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
        records.x = VarIn(formula.nx)
        records.y = VarOut(formula.ny)
 
        patterns = {}
        for i in range(len(template.matches)):
          match = template.matches[i]
          if(isinstance(match, ast.Formula)):
            pvars = match.pvars()
            for k, v in pvars.iteritems():
              patterns[str(i) + "." + k] = v
          elif(isinstance(match, int)):
            patterns[str(i)] = match
 
        records.ps = patterns
 
        return (template.icode_list, records)

  def __repr__(self):
    return "%s(%s, %s)" % (self.__class__.__name__, self.size_rule, 
        self.templates)
 
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
        # f should be an Integer
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
      if isinstance(val, ast.Formula):
        return True
      return val.isConst()
    raise KeyError 

# stuff for symbols in icode:

class NextVarSet:
    def __init__(self):
        #print 'NextVarSet created'
        self.vars = {}

    def __getitem__(self, key):
        if key not in self.vars:
            self.vars[key] = 0
        i = self.vars[key]
        self.vars[key] += 1
        return "%s%d" % (key, i)
        #return i

class Var:
    var_type = 'v'
    next_val = NextVarSet()

    def __init__(self,val=None,name=None):
        self.val = val
        self.name = name
        self.out_name = None

    def num(self):
        if self.val is not None:
            if hasattr(self.val, 'num'):
                return getattr(self.val, 'num')()
            return self.val
        return self

    def __str__(self):
        if self.val is not None:
            if hasattr(self.val, 'num'):
                return str(getattr(self.val, 'num')())
            return str(self.val)
        if not self.name:
            self.name = "%s" % (self.__class__.next_val[self.__class__.var_type])
        return 'Var(%s)' % (self.name)

    #TODO: this needs to be fixed!
    def __mul__(self, other):
        if self.val is not None:
            return self.val * other
        return '%s * %s' % (self.num(), other.num())

    def __rmul__(self, other):
        if self.val is not None:
            return other * self.val
        return '%s * %s' % (other.num(), self.num())

    def __repr__(self):
        return str(self)

#TODO we should construct these dynamically?
class VarR(Var):
    var_type = 'r'

class VarF(Var):
    var_type = 'f'

class DoVar(Var):
    """This is used in Do Loops to indicate the current loop value"""
    def __init__(self,inst,n,val=0):
        self.inst = inst #The instruction this variable is associated with.
        self.n = n # The value that this variable goes up to
        self.val = val #The present value during a particular unrolling step

    def __str__(self):
        return "DoVar(val=%d, n=%d, inst=%d)" % (self.val, self.n, self.inst)


### VECTORS ###
class Vec(Var):
    var_type = 't'
    next_val = NextVarSet()
    def __init__(self, size=None):
        #print "Initializing VECTOR", id(self)
        self.size = size
        self.val = None
        self.name = None
        self.out_name = None

    def __str__(self):
        if self.val is not None:
            if hasattr(self.val, 'num'):
                return str(getattr(self.val, 'num')())
            #return str(self.val)
        if self.name is None:
            self.name = "%s" % (self.__class__.next_val[self.__class__.var_type])
        return '$%s' % (self.name)

    def __len__(self):
        return self.size

class IOVec(Vec):
    def __str__(self):
        return self.var_type

class VarIn(IOVec):
    var_type = 'x'

class VarOut(IOVec):
    var_type = 'y'


class IRef:
    var_type = 'i'
    """This is just a reference to a variable $i0, $i1 ... """
    def __init__(self,ref):
        self.ref = ref

    def __str__(self):
        return "$i%d" % (self.ref)

class Index:
    """This is used to store the index in icode."""
    def __init__(self, vec, exp):
        self.vec = vec
        self.exp = exp

    def idx(self, stack=None):
        #Calculate our accumulator and the multiplies
        accum = self.exp[0]
        idxs = [ e * i for (e, i) in zip(self.exp[1:], stack) ]

        #The multiplies can be either str or int. sum them up or concatenate
        accum += sum([ i for i in idxs if isinstance(i, int) ])
        strs = [ i for i in idxs if isinstance(i, str) ]
        if len(strs):
            s = '+'.join(strs)
            if accum > 0:
                s += "+%d" % (accum)
            if accum < 0:
                s += "-%d" % (-accum)
            return (self.vec, s)
        return (self.vec, accum)

    def num(self):
        return self

    def __str__(self):
        return "Index(%s, %s)" % (self.vec, self.exp)

