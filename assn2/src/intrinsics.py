#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

intrinsics.py

Contains all of the intrinsic scalar functions
"""

import math
import cmath

import numbers

def num(val):
  if isinstance(val, numbers.Number):
    return val
  else:
    return val.num()
  #raise NameError

def Wf(n, k):
  return cmath.exp(2 * cmath.pi * complex(0,1) / n) ** k

def TWf(mn, n, k):
  return Wf(mn, (k/n) * (k % n))

def Cf(n, k):
  return math.cos(2 * k * math.pi / n)

def Sf(n, k):
  return math.sin(2 * k * math.pi / n)

class Intrinsic:
  pass

class W(Intrinsic):
  '''Return \omega_n^k'''
  def __init__(self, n, k):
    self.n = n
    self.k = k

  def num(self):
    #print self.n, num(self.n)
    #print self.k, num(self.k)
    return Wf(num(self.n),num(self.k))

  def __str__(self):
    return "W(%s %s)" % (self.n, self.k)
    #return str(id(self))

class WR(Intrinsic):
  '''Return the real part of \omega_n^k'''
  def __init__(self, n, k):
    self.n = n
    self.k = k

  def num(self):
    return Wf(num(self.n),num(self.k)).real

  def __str__(self):
    return "WR(%s %s)" % (self.n, self.k)

class WI(Intrinsic):
  '''Return the imaginary part of \omega_n^k'''
  def __init__(self, n, k):
    self.n = n
    self.k = k

  def num(self):
    return Wf(num(self.n),num(self.k)).imag

  def __str__(self):
    return "WI(%s %s)" % (self.n, self.k)

class TW(Intrinsic):
  '''Return the kth diagonal element of T_n^{mn}'''
  def __init__(self, mn, n, k):
    self.mn = mn
    self.n = n
    self.k = k

  def num(self):
    return TWf(num(self.mn),num(self.n),num(self.k))

  def __str__(self):
    return "TW(%s %s %s)" % (self.mn, self.n, self.k)

class TWR(Intrinsic):
  def __init__(self, mn, n, k):
    self.mn = mn
    self.n = n
    self.k = k

  def num(self):
    return TWf(num(self.mn),num(self.n),num(self.k)).real

  def __str__(self):
    return "TWR(%s %s %s)" % (self.mn, self.n, self.k)

class TWI(Intrinsic):
  def __init__(self, mn, n, k):
    self.mn = mn
    self.n = n
    self.k = k

  def num(self):
    return TWf(num(self.mn),num(self.n),num(self.k)).imag

  def __str__(self):
    return "TWI(%s %s %s)" % (self.mn, self.n, self.k)

class C(Intrinsic):
  def __init__(self, n, k):
    self.n = n
    self.k = k

  def num(self):
    return Cf(num(self.n),num(self.k))

  def __str__(self):
    return "C(%s %s)" % (self.n, self.k)

class S(Intrinsic):
  def __init__(self, n, k):
    self.n = n
    self.k = k

  def num(self):
    return Sf(num(self.n),num(self.k))

  def __str__(self):
    return "S(%s %s)" % (self.n, self.k)
