def ICode:
  def __str__(self):
    return repr(self)

def Nop(ICode):
  def __repr__(self):
    return "nop()"

def Add(ICode):
  def __init__(src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "add(%s, %s, %s)" % (self.src1, self.src2, self.dest)

def Sub(ICode):
  def __init__(src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "sub(%s, %s, %s)" % (self.src1, self.src2, self.dest)

def Mul(ICode):
  def __init__(src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "mul(%s, %s, %s)" % (self.src1, self.src2, self.dest)

def Div(ICode):
  def __init__(src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "div(%s, %s, %s)" % (self.src1, self.src2, self.dest)

def Mod(ICode):
  def __init__(src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "mod(%s, %s, %s)" % (self.src1, self.src2, self.dest)

def Copy(ICode):
  def __init__(src1, dest):
    self.src1 = src1
    self.dest = dest

  def __repr__(self):
    return "copy(%s, %s)" % (self.src1, self.dest)

def Call(ICode):
  def __init__(src1, src2, dest):
    self.src1 = src1
    self.src2 = src2
    self.dest = dest

  def __repr__(self):
    return "call(%s, %s, %s)" % (self.src1, self.src2, self.dest)

def Do(ICode):
  def __init__(src1, dest):
    self.src1 = src1

  def __repr__(self):
    return "dounroll(%s)" % (self.src1)

def Do(ICode):
  def __init__(src1, dest):
    self.src1 = src1

  def __repr__(self):
    return "do(%s)" % (self.src1)

def End(ICode):
  def __repr__(self):
    return "end()"

def DefTmp(ICode):
  def __init__(src1, src2, dest):
    self.src1 = src1

  def __repr__(self):
    return "deftmp(%s)" % (self.src1)

# Need to keep track of a LoopIdx stack
# Need to keep track of a Temp stack

class Var:
  def __init__(self):
    self.val = None

class VarR(Var): pass

class VarF(Var): pass

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
def F(in_v, out_v, p1, i_stack):
  r0 = VarR()
  r1 = VarR()
  r2 = VarR()
  r3 = VarR()
  f0 = VarF()
  return [ Do(p1),
           Copy(0, out_v[ [0,1] ] ),
           Do(p1),
           Mul(i_stack[0], i_stack[1], r0),
           Div(r0, p1, r1),
           Mul(r1, p1, r2),
           Sub(r0, r2, r3),
           Mul( W(p1, r3), in_v[ [0,1,0] ], f0 ),
           Add( out_v[ [0,0,1] ], f0, out_v[ [0,0,1] ]),
           End(),
           End() ]

# (template (I ANY)		;; ---- I(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
# 		  $y(0 1) = $x(0 1)
# 		end
# 	))
def I(in_v, out_v, p1, i_stack):
  return [ Do(p1),
           Copy(in_v[ [0,1] ], out_v[ [0,1] ]),
           End() ]

# (template (J ANY)		;; ---- J(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
#                  $r0 = $p1-1
# 		  $y(0 1) = $x($r0 (-1))
# 		end
# 	))
def J(in_v, out_v, p1, i_stack):
  pass


# (template (O ANY)		;; ---- O(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
# 		  $y(0 1) = 0
# 		end
# 	))
def O(in_v, out_v, p1, i_stack):
  pass


#T

#L

#compose
#tensor
#direct_sum
#matrix
#diagonal
#permutation
#rpermutation
#sparse
#conjugate
#scale
