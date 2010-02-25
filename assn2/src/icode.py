#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

icodes.py

"""

import numbers

from intrinsics import *
from icode_vars import *
from symbol_collection import SymbolCollection

class ICode:
  def __str__(self):
    return repr(self)

class Nop(ICode):
  """Nops are used to replace unnecessary instructions"""
  def __repr__(self):
    return "nop()"

class OpICode(ICode):
  """This is used to better categorize all of the Arithmetic Operation
  instructions"""
  pass

class Add(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "add(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Sub(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "sub(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Mul(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "mul(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Div(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "div(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Mod(OpICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "mod(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class Copy(ICode):
  def __init__(self, src1, dest):
    self.src1 = src1
    self.dest = dest

  def __repr__(self):
    return "copy(%s, %s)" % (self.src1, self.dest)

class Call(ICode):
  def __init__(self, src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "call(%s, %s, %s)" % (self.src1, self.src2, self.dest)

class DoUnroll(ICode):
  def __init__(self, src1):
    self.src1 = src1

  def __repr__(self):
    return "dounroll(%s)" % (self.src1)

class Do(ICode):
  def __init__(self, src1):
    self.src1 = src1

  def __repr__(self):
    return "do(%s)" % (self.src1)

class End(ICode):
  def __repr__(self):
    return "end()"

class DefTmp(ICode):
  def __init__(self, src1):
    self.src1 = src1

  def __repr__(self):
    return "deftmp(%s)" % (self.src1)

#TODO Need to keep track of a LoopIdx stack
#TODO Need to keep track of a Temp stack

def num(val):
  if isinstance(val, numbers.Number):
    return val
  else:
    return val.num()
  #raise NameError

def isnumeric(val):
  return isinstance(val, numbers.Number)

class ICodeList:
  def __init__(self, icodes):
    self.icodes = icodes

  def varunroll(self, old, stack, varmap, outvar=False):
    if isinstance(old, numbers.Number):
      return old
    elif isinstance(old, Intrinsic):
      #n, k, mn
      if hasattr(old, 'n'):
        old.n = self.varunroll(old.n, stack, varmap, False)
      if hasattr(old, 'k'):
        old.k = self.varunroll(old.k, stack, varmap, False)
      if hasattr(old, 'mn'):
        old.mn = self.varunroll(old.mn, stack, varmap, False)
      return old
    elif isinstance(old, Vec):
      return old
    elif isinstance(old, Index):
      if isinstance(old.vec, Vec):
        if isinstance(old.exp, list):
          return Index(old.vec, old.exp, stack)
      return old
    elif isinstance(old, DoVar):
      raise TypeError
    elif isinstance(old, IRef):
      return stack[old.val].val
    #We want to do SSA. If we are an output variable, create
    #a new map. Otherwise we want to use our old value.
    elif outvar:
      varmap[old] = old.__class__(old.val, old.name)
      return varmap[old]
    elif old in varmap:
      return varmap[old]
    else:
      return old

  def unroll(self):
    unrolled = []
    stack = []
    varmap = {}
    i = 0
    while i < len(self.icodes):
      inst = self.icodes[i]

      #LOOPS
      if isinstance(inst, Do):
        stack.insert(0, DoVar(i,inst.src1))
      elif isinstance(inst, End):
        stack[0].val += 1
        #if < then we still have to loop, otherwise move on
        if stack[0].val < stack[0].n:
          i = stack[0].inst
        else:
          stack = stack[1:]

      elif isinstance(inst, Call):
        #TODO
        pass

      elif isinstance(inst, DefTmp):
        unrolled.append(DefTmp(inst.src1))
        #TODO

      #OPERATIONS
      elif isinstance(inst, OpICode):
        src1 = self.varunroll(inst.src1, stack, varmap, False)
        src2 = self.varunroll(inst.src2, stack, varmap, False)
        dest = self.varunroll(inst.dest, stack, varmap, True)
        unrolled.append(inst.__class__(src1, src2, dest))
      elif isinstance(inst, Copy):
        src1 = self.varunroll(inst.src1, stack, varmap, False)
        dest = self.varunroll(inst.dest, stack, varmap, True)
        unrolled.append(Copy(src1, dest))
      i+=1

    self.icodes = unrolled

  def constprop(self):
    i = 0
    while i < len(self.icodes):
      inst = self.icodes[i]

      if isinstance(inst, OpICode):
        src1 = num(inst.src1)
        src2 = num(inst.src2)
        if src1:
          inst.src1 = src1
        if src2:
          inst.src2 = src2
        if isinstance(inst, Add):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 + src2
            self.icodes[i] = None
          elif src1 == 0:
            inst.dest.val = src2
            self.icodes[i] = None
          elif src2 == 0:
            inst.dest.val = src1
            self.icodes[i] = None

        elif isinstance(inst, Sub):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 - src2
            self.icodes[i] = None
          elif src2 == 0:
            inst.dest.val = src1
            self.icodes[i] = None

        elif isinstance(inst, Mul):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 * src2
            self.icodes[i] = None
          elif src1 == 0 or src2 == 0:
            inst.dest.val = 0
            self.icodes[i] = None

        elif isinstance(inst, Div):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 / src2
            self.icodes[i] = None
          elif src1 == 0:
            inst.dest.val = 0
            self.icodes[i] = None
          elif src2 == 0:
            raise ZeroDivisionError

        elif isinstance(inst, Mod):
          if isnumeric(src1) and isnumeric(src2):
            inst.dest.val = src1 % src2
            self.icodes[i] = None
          elif src1 == 0:
            inst.dest.val = 0
            self.icodes[i] = None
          elif src2 == 0:
            raise ZeroDivisionError

      elif isinstance(inst, Copy):
        src1 = num(inst.src1)
        if src1:
          inst.dest.val = src1.val

      i+=1
    self.icodes = [i for i in self.icodes if i]

#loop stack is just a list with the first element being the top

##### ICODE TEMPLATES #####

# (template (F ANY)		;; ---- F(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
# 		  $y(0 1) = 0
# 		  do $p1
# 		    $r0 = $i0 * $i1
# 		    $r1 = $r0 / $p1
# 		    $r2 = $r1 * $p1
# 		    $r3 = $r0 - $r2
# 		    $f0 = W($p1 $r3) * $x(0 1 0)
# 		    $y(0 0 1) = $y(0 0 1) + $f0
# 		  end
# 		end
# 	))
def F(in_v, out_v, p1):
  r0 = VarR()
  r1 = VarR()
  r2 = VarR()
  r3 = VarR()
  f0 = VarF()
  return [ Do(p1),
           Copy(0, Index(out_v, [0,1])),
           Do(p1),
           Mul(IRef(0), IRef(1), r0),
           Div(r0, p1, r1),
           Mul(r1, p1, r2),
           Sub(r0, r2, r3),
           Mul(W(p1, r3), Index(in_v, [0,1,0]), f0 ),
           Add(Index(out_v, [0,0,1]), f0, Index(out_v, [0,0,1])),
           End(),
           End() ]

# (template (I ANY)		;; ---- I(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
# 		  $y(0 1) = $x(0 1)
# 		end
# 	))
def I(in_v, out_v, p1):
  return [ Do(p1),
           Copy(Index(in_v, [0,1]), Index(out_v, [0,1])),
           End() ]

# (template (J ANY)		;; ---- J(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
#                  $r0 = $p1-1
# 		  $y(0 1) = $x($r0 (-1))
# 		end
# 	))
def J(in_v, out_v, p1):
  r0 = VarR()
  return [ Do(p1),
           Sub(p1, 1, r0),
           Copy(Index(in_v, [r0, -1]), Index(out_v, [0, 1])),
           End() ]

# (template (O ANY)		;; ---- O(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
# 		  $y(0 1) = 0
# 		end
# 	))
def O(in_v, out_v, p1):
  return [ Do(p1),
           Copy (0, Index(out_v, [0,1])),
           End() ]


#(template (T ANY ANY) 		;; ---- T(mn n) parameters: self(ny,nx), mn, n
#	[$p1>=1 && $p2>=1 && $p1%$p2==0]
#	(
#		do $p1
#		  $r0 = $i0
#	          $y(0 1) = TW($p1 $p2 $r0) * $x(0 1)
#		end
#	))
def T(in_v, out_v, p1, p2):
  r0 = VarR()
  return [ Do(p1),
           Copy (IRef(0), r0),
           Mul (TW(p1, p2, r0), Index(in_v, [0,1]), Index(out_v, [0,1])),
           End() ]


#(template (L ANY ANY)		;; ---- L(mn n) parameters: self(ny,nx), mn, n
#	[$p1>=1 && $p2>=1 && $p1%$p2==0]
#	(
#		$r0 = $p1 / $p2
#		do $p2
#		  do $r0
#		    $y(0 1 $r0) = $x(0 $p2 1)
#		  end
#		end
#	))
def L(in_v, out_v, p1, p2):
  r0 = VarR()
  return [ Div(p1, p2, r0),
           Do(p2),
           Do(r0),
           Copy(Index(in_v, [0,p2,1]), Index(out_v, [0, 1, r0])),
           End(),
           End() ]

#(template (compose any any) 
#		;; ---- Amn * Bpq parameters: self(ny,nx), A(m,n), B(p,q)
#	(			 
#		deftemp $p2.ny
#compose
#		$t0(0:1:$p2.ny_1) = call $p2( $x(0:1:$p2.nx_1) )
#		$y(0:1:$p1.ny_1)  = call $p1( $t0(0:1:$p1.nx_1) )
#	))
def compose(in_v, out_v, p1, p2):
  t0 = Vec () # needs to be size p2.ny ??
  return [  Call (p2, in_v, t0),
            Call (p1, t0, out_v) ]

#(template (tensor any any)
#		;; ---- Amn x Bpq parameters: self(ny,nx), A(m,n), B(p,q)
#	(
#		$r0 = $p1.nx * $p2.ny
#		$r1 = $r0 - 1
#		deftemp $r0
#		do $p1.nx
#		  $t0(0:1:$p2.ny_1 $p2.ny) = call $p2( $x(0:1:$p2.nx_1 $p2.nx) )
#		end
#		do $p2.ny
#		  $y(0:$p2.ny:$p0.ny_1 1) = call $p1( $t0(0:$p2.ny:$r1 1) )
#		end
#	))
def tensor (in_v, out_v, p1, p2):
  r0 = VarR();
  r1 = VarR();
  t0 = Vec();
  return [ Mul (p1.nx, p2,ny, r0), # ???
           Sub (r0, 1, r1),
           # set the size of t0 to $r0 ???,
           Do (p1.nx),
           Call (p2, in_v, t0),
           End (),
           Do (p2.ny),
           Call (p1, t0, out_v),
           End () ]
  

#(template (direct_sum any any)  
#		;; ---- Amn + Bpq parameters: self(ny,nx), A(mn,n), B(p,q)
#	(
#		$y(0:1:$p1.ny_1) = call $p1( $x(0:1:$p1.nx_1) )
#		$y($p1.ny:1:$p0.ny_1) = call $p2( $x($p1.nx:1:$p0.nx_1) )
#	))
def direct_sum (in_v, out_v, p1, p2):
  return [ Call (p1, in_v, out_v),
           Call (p2, in_v, out_v) ]

#(template (matrix (0))		;; ---- matrix parameters: self(ny,nx), matrix
#       ;; format: (matrix (a11 ... a1n) ... (am1 ... amn))
#	(
#		dounroll $p1.ny
#		  $y(0 1) = 0
#		  do $p1.nx
#		    $f0 = $p1.a($i1 $i0) * $x(0 1 0)
#		    $y(0 0 1) = $y(0 0 1) + $f0
#		  end
#		end
#	))
def matrix(in_v, out_v, p1):
  f0 = VarF()
  return [ Copy (0, Index(out_v, [0,1])),
           Do (p1.nx),
           Mul (Index (p1, [IRef(1), IRef(0)]), Index(in_v, [0,1,0]), f0),
           Add (Index(out_v, [0,0,1]), f0, Index(out_v, [0,0,1])),
           End (),
           End () ]


#(template (diagonal (0))	;; ---- diagonal parameters: self(ny,nx), diag
#       ;; format: (diagonal (a11 ... amm))
#	(
#		dounroll $p1.ny
#		  $y(0 1) = $p1.a(0 $i0) * $x(0 1)
#		end
#	))
def diagonal (in_v, out_v, p1):
  return [ Do (p1.ny),
           Mul (Index (p1, [0, IRef(0)]), Index(in_v, [0,1]), Index (out_v, [0,1])),
           End () ]
  
#(template (permutation (0))	;; ---- permutation parameters: self(ny,nx), perm
#       ;; format: (permutation (p1 ... pn)), 1<=pi<=n
#	(
#		dounroll $p1.ny
#		  $r0 = $p1.a(0 $i0) - 1
#		  $y(0 1) = $x($r0 0)
#		end
#	))
def permutation (in_v, out_v, p1):
  r0 = VarR()
  return [ Do (p1.ny),
           Sub (Index (p1, [0,IRef(0)]), 1, r0),
           Copy (Index (in_v, [r0,1]), Index (out_v, [0,1])),
           End () ]
  
#(template (rpermutation (0))	;; ---- rpermutation parameters: self(ny,nx),rperm
#       ;; format: (rpermutation (p1 ... pn)), 1<=pi<=n
#	(
#		dounroll $p1.ny
#		  $r0 = $p1.a(0 $i0) - 1
#		  $y($r0 0) = $x(0 1)
#		end
#	))
def rpermutation (in_v, out_v, p1):
  r0 = VarR()
  return [ Do (p1.ny),
           Sub (Index (p1, [0,IRef(0)]), 1, r0),
           Copy (Index (in_v, [0,1]), Index(out_v, [r0, 0])),
           End () ]

#sparse
#(template (sparse (0))		;; ---- sparse parameters: self(ny,nx), sp-matrix
#       ;; format: (sparse (i j aij) ... ), 1<=i<=ny, 1<=j<=nx
#	(
#		dounroll $p1.ny
#		  $y(0 1) = 0
#		end
#		dounroll $p1.matrix_nrow
#		  $r0 = $p1.a($i0 0)-1
#		  $r1 = $p1.a($i0 1)-1
#		  $f1 = $p1.a($i0 2)*$x($r1 0)
#		  $y($r0 0) = $y($r0 0)+$f1	 
#		end
#	))
def sparse (in_v, out_v, p1):
  r0 = VarR()
  r1 = VarR()
  f1 = VarF()
  return [ Do (p1.ny),
           Copy (0, Index (out_v, [0,1])),
           End (),
           Do (p1.matrix_nrow),
           Sub (Index (p1, [IRef(0), 0]), 1, r0),
           Sub (Index (p1, [IRef(0), 1]), 1, r1),
           Mul (Index (p1, [IRef(0), 2]), Index (in_v, [r1, 0]), f1),
           Add (Index (out_v, [r0, 0]), f1, Index (out_v, [r0,0])),
           End () ]

#conjugate


#scale
def scale (in_v, out_v, p1, p2):
  t0 = Vec()  #size should be p2.ny
  return [ Call (p2, in_v, t0),
           Do (p2.ny)
           Mul (p1, Index (t0, [0,1]), Index, (out_v, [0,1]),
           End () ]
