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

SPL_SHAPE_SQUARE   = 0
SPL_SHAPE_RECT     = 1
SPL_SHAPE_DIAG     = 2
SPL_SHAPE_RECTDIAG = 3

SPL_SIZE_IDENT	   = 0
SPL_SIZE_TRANSPOSE = 1
SPL_SIZE_COMPOSE   = 2
SPL_SIZE_SUM       = 3
SPL_SIZE_TENSOR    = 4
SPL_SIZE_MATRIX    = 5
SPL_SIZE_VECTOR    = 6
SPL_SIZE_SPARSE    = 7

F_SHAPE            = SPL_SHAPE_SQUARE
I_SHAPE            = SPL_SHAPE_RECTDIAG
O_SHAPE            = SPL_SHAPE_RECTDIAG
T_SHAPE            = SPL_SHAPE_DIAG
L_SHAPE            = SPL_SHAPE_SQUARE
J_SHAPE            = SPL_SHAPE_SQUARE

COMPOSE_SIZE       = SPL_SIZE_COMPOSE
TENSOR_SIZE        = SPL_SIZE_TENSOR
DIRECT_SUM_SIZE    = SPL_SIZE_SUM
CONJUGATE_SIZE     = SPL_SIZE_COMPOSE
SCALE_SIZE         = SPL_SIZE_TENSOR

MATRIX_SIZE        = SPL_SIZE_MATRIX
DIAGONAL_SIZE      = SPL_SIZE_VECTOR
PERMUTATION_SIZE   = SPL_SIZE_VECTOR
RPERMUTATION_SIZE  = SPL_SIZE_VECTOR
SPARSE_SIZE        = SPL_SIZE_SPARSE

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
def F(p1, x=VarIn(), y=VarOut()):
  r0 = VarR()
  r1 = VarR()
  r2 = VarR()
  r3 = VarR()
  f0 = VarF()
  return [ Do(p1),
           Copy(0, Index(y, [0,1])),
           Do(p1),
           Mul(IRef(0), IRef(1), r0),
           Div(r0, p1, r1),
           Mul(r1, p1, r2),
           Sub(r0, r2, r3),
           Mul(W(p1, r3), Index(x, [0,1,0]), f0 ),
           Add(Index(y, [0,0,1]), f0, Index(y, [0,0,1])),
           End(),
           End() ]

def F_size(p1):
  return p1, p1

# (template (I ANY)		;; ---- I(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
# 		  $y(0 1) = $x(0 1)
# 		end
# 	))
def I(p1, x=VarIn(), y=VarOut()):
  return [ Do(p1),
           Copy(Index(x, [0,1]), Index(y, [0,1])),
           End() ]

def I_size(p1):
  return p1, p1


# (template (J ANY)		;; ---- J(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
#                  $r0 = $p1-1
# 		  $y(0 1) = $x($r0 (-1))
# 		end
# 	))
def J(p1, x=VarIn(), y=VarOut()):
  r0 = VarR()
  return [ Do(p1),
           Sub(p1, 1, r0),
           Copy(Index(x, [r0, -1]), Index(y, [0, 1])),
           End() ]

def J_size(p1):
  return p1, p1


# (template (O ANY)		;; ---- O(n) parameters: self(ny,nx), n
#        [$p1>=1]
# 	(
# 		do $p1
# 		  $y(0 1) = 0
# 		end
# 	))
def O(p1, x=VarIn(), y=VarOut()):
  return [ Do(p1),
           Copy(0, Index(y, [0,1])),
           End() ]

def O_size(p1):
  return p1, p1

#(template (T ANY ANY) 		;; ---- T(mn n) parameters: self(ny,nx), mn, n
#	[$p1>=1 && $p2>=1 && $p1%$p2==0]
#	(
#		do $p1
#		  $r0 = $i0
#	          $y(0 1) = TW($p1 $p2 $r0) * $x(0 1)
#		end
#	))
def T(p1, p2, x=VarIn(), y=VarOut()):
  r0 = VarR()
  return [ Do(p1),
           Mul(TW(p1, p2, IRef(0)), Index(x, [0,1]), Index(y, [0,1])),
           End() ]

def T_size(p1, p2):
  return p1, p1

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
def L(p1, p2, x=VarIn(), y=VarOut()):
  r0 = VarR()
  return [ Div(p1, p2, r0),
           Do(p2),
           Do(r0),
           Copy(Index(x, [0,p2,1]), Index(y, [0, 1, r0])),
           End(),
           End() ]

def L_size(p1, p2):
  return p1, p1

#(template (compose any any)
#		;; ---- Amn * Bpq parameters: self(ny,nx), A(m,n), B(p,q)
#	(
#		deftemp $p2.ny
#		$t0(0:1:$p2.ny_1) = call $p2( $x(0:1:$p2.nx_1) )
#		$y(0:1:$p1.ny_1)  = call $p1( $t0(0:1:$p1.nx_1) )
#	))
def compose(p1, p2, x=VarIn(), y=VarOut()):
  t0 = Vec()
  return [ Call(p2, x, t0),
           Call(p1, t0, y) ]

def compose_size(p1, p2):
  return p2.nx, p1.ny
  
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
# def tensor (p1, p2, x=VarIn(), y=VarOut()):
#   r0 = VarR();
#   r1 = VarR();
#   t0 = Vec();
#   return [ Mul (p1.nx, p2,ny, r0), # ???
#            Sub (r0, 1, r1),
#            # set the size of t0 to $r0 ???,
#            Do (p1.nx),
#            Call (p2, x, t0),
#            End (),
#            Do (p2.ny),
#            Call (p1, t0, y),
#            End () ]

#(template (direct_sum any any)
#		;; ---- Amn + Bpq parameters: self(ny,nx), A(mn,n), B(p,q)
#	(
#		$y(0:1:$p1.ny_1) = call $p1( $x(0:1:$p1.nx_1) )
#		$y($p1.ny:1:$p0.ny_1) = call $p2( $x($p1.nx:1:$p0.nx_1) )
#	))
#def direct_sum (x, y, p1, p2):
#  return [ Call (p1, x, y),
#           Call (p2, x, y) ]
#

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
# def matrix(x, y, p1):
#   f0 = VarF()
#   return [ Copy (0, Index(y, [0,1])),
#            Do (p1.nx),
#            Mul (Index (p1, [IRef(1), IRef(0)]), Index(x, [0,1,0]), f0),
#            Add (Index(y, [0,0,1]), f0, Index(y, [0,0,1])),
#            End (),
#            End () ]


# #(template (diagonal (0))	;; ---- diagonal parameters: self(ny,nx), diag
# #       ;; format: (diagonal (a11 ... amm))
# #	(
# #		dounroll $p1.ny
# #		  $y(0 1) = $p1.a(0 $i0) * $x(0 1)
# #		end
# #	))
# def diagonal (x, y, p1):
#   return [ Do (p1.ny),
#            Mul (Index (p1, [0, IRef(0)]), Index(x, [0,1]), Index (y, [0,1])),
#            End () ]

# #(template (permutation (0))	;; ---- permutation parameters: self(ny,nx), perm
# #       ;; format: (permutation (p1 ... pn)), 1<=pi<=n
# #	(
# #		dounroll $p1.ny
# #		  $r0 = $p1.a(0 $i0) - 1
# #		  $y(0 1) = $x($r0 0)
# #		end
# #	))
# def permutation (x, y, p1):
#   r0 = VarR()
#   return [ Do (p1.ny),
#            Sub (Index (p1, [0,IRef(0)]), 1, r0),
#            Copy (Index (x, [r0,1]), Index (y, [0,1])),
#            End () ]

# #(template (rpermutation (0))	;; ---- rpermutation parameters: self(ny,nx),rperm
# #       ;; format: (rpermutation (p1 ... pn)), 1<=pi<=n
# #	(
# #		dounroll $p1.ny
# #		  $r0 = $p1.a(0 $i0) - 1
# #		  $y($r0 0) = $x(0 1)
# #		end
# #	))
# def rpermutation (x, y, p1):
#   r0 = VarR()
#   return [ Do (p1.ny),
#            Sub (Index (p1, [0,IRef(0)]), 1, r0),
#            Copy (Index (x, [0,1]), Index(y, [r0, 0])),
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
# def sparse (x, y, p1):
#   r0 = VarR()
#   r1 = VarR()
#   f1 = VarF()
#   return [ Do (p1.ny),
#            Copy (0, Index (y, [0,1])),
#            End (),
#            Do (p1.matrix_nrow),
#            Sub (Index (p1, [IRef(0), 0]), 1, r0),
#            Sub (Index (p1, [IRef(0), 1]), 1, r1),
#            Mul (Index (p1, [IRef(0), 2]), Index (x, [r1, 0]), f1),
#            Add (Index (y, [r0, 0]), f1, Index (y, [r0,0])),
#            End () ]

# #conjugate


# def scale(p1, p2, x=VarIn(), y=VarOut()):
#   t0 = Vec()  #size should be p2.ny
#   return [ Call (p2, x, t0),
#            Do (p2.ny)
#            Mul (p1, Index (t0, [0,1]), Index, (y, [0,1]),
#            End () ]
