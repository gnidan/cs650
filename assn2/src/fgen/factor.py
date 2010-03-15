#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

factor.py

Routines for factoring integers
"""
import math
from memoize import memoize

#http://www.stealthcopter.com/blog/2009/11/python-factors-of-a-number/
@memoize
def factors(n):
	# 1 and n are automatically factors of n
	#fact=[1,n]
  fact=[]
	# starting at 2 as we have already dealt with 1
  check=2
	# calculate the square root of n and use this as the
	# limit when checking if a number is divisible as
	# factors above sqrt(n) will already be calculated as
	# the inverse of a lower factor IE. finding factors of
	# 100 only need go up to 10 (sqrt(100)=10) as factors
	# such as 25 can be found when 5 is found to be a
	# factor 100/5=25
  rootn=math.sqrt(n)
  while check<rootn:
    if n%check==0:
      fact.append(check)
      fact.append(n/check)
    check+=1
	# this line checks the sqrt of the number to see if
	# it is a factor putting it here prevents it appearing
	# twice in the above while loop and putting it outside
	# the loop should save some time.
  if rootn==check:
    fact.append(check)
	# return an array of factors sorted into numerial order.
  fact.sort()
  return fact

@memoize
def isprime(n):
	"""A prime number 'n' only has 2 factors (1, n)."""
	return len(factors(n)) == 0

@memoize
def primefactors(n):
	return [i for i in factors(n) if isprime(i)]
