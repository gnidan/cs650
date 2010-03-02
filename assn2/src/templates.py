#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

templates.py icode templates hand coded in Pyhton functions
"""

from symbols import *
from icode import *
from intrinsics import *

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
def F(p, in_v=VarIn(), out_v=VarOut()):
  p1 = p[0]
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


# #(template (T ANY ANY) 		;; ---- T(mn n) parameters: self(ny,nx), mn, n
# #	[$p1>=1 && $p2>=1 && $p1%$p2==0]
# #	(
# #		do $p1
# #		  $r0 = $i0
# #	          $y(0 1) = TW($p1 $p2 $r0) * $x(0 1)
# #		end
# #	))
# def T(in_v, out_v, p1, p2):
#   r0 = VarR()
#   return [ Do(p1),
#            Copy (IRef(0), r0),
#            Mul (TW(p1, p2, r0), Index(in_v, [0,1]), Index(out_v, [0,1])),
#            End() ]


# #(template (L ANY ANY)		;; ---- L(mn n) parameters: self(ny,nx), mn, n
# #	[$p1>=1 && $p2>=1 && $p1%$p2==0]
# #	(
# #		$r0 = $p1 / $p2
# #		do $p2
# #		  do $r0
# #		    $y(0 1 $r0) = $x(0 $p2 1)
# #		  end
# #		end
# #	))
# def L(in_v, out_v, p1, p2):
#   r0 = VarR()
#   return [ Div(p1, p2, r0),
#            Do(p2),
#            Do(r0),
#            Copy(Index(in_v, [0,p2,1]), Index(out_v, [0, 1, r0])),
#            End(),
#            End() ]

# #(template (compose any any)
# #		;; ---- Amn * Bpq parameters: self(ny,nx), A(m,n), B(p,q)
# #	(
# #		deftemp $p2.ny
# #compose
# #		$t0(0:1:$p2.ny_1) = call $p2( $x(0:1:$p2.nx_1) )
# #		$y(0:1:$p1.ny_1)  = call $p1( $t0(0:1:$p1.nx_1) )
# #	))
# def compose(in_v, out_v, p1, p2):
#   t0 = Vec () # needs to be size p2.ny ??
#   return [  Call (p2, in_v, t0),
#             Call (p1, t0, out_v) ]

# #(template (tensor any any)
# #		;; ---- Amn x Bpq parameters: self(ny,nx), A(m,n), B(p,q)
# #	(
# #		$r0 = $p1.nx * $p2.ny
# #		$r1 = $r0 - 1
# #		deftemp $r0
# #		do $p1.nx
# #		  $t0(0:1:$p2.ny_1 $p2.ny) = call $p2( $x(0:1:$p2.nx_1 $p2.nx) )
# #		end
# #		do $p2.ny
# #		  $y(0:$p2.ny:$p0.ny_1 1) = call $p1( $t0(0:$p2.ny:$r1 1) )
# #		end
# #	))
# def tensor (in_v, out_v, p1, p2):
#   r0 = VarR();
#   r1 = VarR();
#   t0 = Vec();
#   return [ Mul (p1.nx, p2,ny, r0), # ???
#            Sub (r0, 1, r1),
#            # set the size of t0 to $r0 ???,
#            Do (p1.nx),
#            Call (p2, in_v, t0),
#            End (),
#            Do (p2.ny),
#            Call (p1, t0, out_v),
#            End () ]


# #(template (direct_sum any any)
# #		;; ---- Amn + Bpq parameters: self(ny,nx), A(mn,n), B(p,q)
# #	(
# #		$y(0:1:$p1.ny_1) = call $p1( $x(0:1:$p1.nx_1) )
# #		$y($p1.ny:1:$p0.ny_1) = call $p2( $x($p1.nx:1:$p0.nx_1) )
# #	))
# def direct_sum (in_v, out_v, p1, p2):
#   return [ Call (p1, in_v, out_v),
#            Call (p2, in_v, out_v) ]

# #(template (matrix (0))		;; ---- matrix parameters: self(ny,nx), matrix
# #       ;; format: (matrix (a11 ... a1n) ... (am1 ... amn))
# #	(
# #		dounroll $p1.ny
# #		  $y(0 1) = 0
# #		  do $p1.nx
# #		    $f0 = $p1.a($i1 $i0) * $x(0 1 0)
# #		    $y(0 0 1) = $y(0 0 1) + $f0
# #		  end
# #		end
# #	))
# def matrix(in_v, out_v, p1):
#   f0 = VarF()
#   return [ Copy (0, Index(out_v, [0,1])),
#            Do (p1.nx),
#            Mul (Index (p1, [IRef(1), IRef(0)]), Index(in_v, [0,1,0]), f0),
#            Add (Index(out_v, [0,0,1]), f0, Index(out_v, [0,0,1])),
#            End (),
#            End () ]


# #(template (diagonal (0))	;; ---- diagonal parameters: self(ny,nx), diag
# #       ;; format: (diagonal (a11 ... amm))
# #	(
# #		dounroll $p1.ny
# #		  $y(0 1) = $p1.a(0 $i0) * $x(0 1)
# #		end
# #	))
# def diagonal (in_v, out_v, p1):
#   return [ Do (p1.ny),
#            Mul (Index (p1, [0, IRef(0)]), Index(in_v, [0,1]), Index (out_v, [0,1])),
#            End () ]

# #(template (permutation (0))	;; ---- permutation parameters: self(ny,nx), perm
# #       ;; format: (permutation (p1 ... pn)), 1<=pi<=n
# #	(
# #		dounroll $p1.ny
# #		  $r0 = $p1.a(0 $i0) - 1
# #		  $y(0 1) = $x($r0 0)
# #		end
# #	))
# def permutation (in_v, out_v, p1):
#   r0 = VarR()
#   return [ Do (p1.ny),
#            Sub (Index (p1, [0,IRef(0)]), 1, r0),
#            Copy (Index (in_v, [r0,1]), Index (out_v, [0,1])),
#            End () ]

# #(template (rpermutation (0))	;; ---- rpermutation parameters: self(ny,nx),rperm
# #       ;; format: (rpermutation (p1 ... pn)), 1<=pi<=n
# #	(
# #		dounroll $p1.ny
# #		  $r0 = $p1.a(0 $i0) - 1
# #		  $y($r0 0) = $x(0 1)
# #		end
# #	))
# def rpermutation (in_v, out_v, p1):
#   r0 = VarR()
#   return [ Do (p1.ny),
#            Sub (Index (p1, [0,IRef(0)]), 1, r0),
#            Copy (Index (in_v, [0,1]), Index(out_v, [r0, 0])),
#            End () ]

# #sparse
# #(template (sparse (0))		;; ---- sparse parameters: self(ny,nx), sp-matrix
# #       ;; format: (sparse (i j aij) ... ), 1<=i<=ny, 1<=j<=nx
# #	(
# #		dounroll $p1.ny
# #		  $y(0 1) = 0
# #		end
# #		dounroll $p1.matrix_nrow
# #		  $r0 = $p1.a($i0 0)-1
# #		  $r1 = $p1.a($i0 1)-1
# #		  $f1 = $p1.a($i0 2)*$x($r1 0)
# #		  $y($r0 0) = $y($r0 0)+$f1
# #		end
# #	))
# def sparse (in_v, out_v, p1):
#   r0 = VarR()
#   r1 = VarR()
#   f1 = VarF()
#   return [ Do (p1.ny),
#            Copy (0, Index (out_v, [0,1])),
#            End (),
#            Do (p1.matrix_nrow),
#            Sub (Index (p1, [IRef(0), 0]), 1, r0),
#            Sub (Index (p1, [IRef(0), 1]), 1, r1),
#            Mul (Index (p1, [IRef(0), 2]), Index (in_v, [r1, 0]), f1),
#            Add (Index (out_v, [r0, 0]), f1, Index (out_v, [r0,0])),
#            End () ]

# #conjugate


# #scale
# def scale (in_v, out_v, p1, p2):
#   t0 = Vec()  #size should be p2.ny
#   return [ Call (p2, in_v, t0),
#            Do (p2.ny)
#            Mul (p1, Index (t0, [0,1]), Index, (out_v, [0,1]),
#            End () ]
