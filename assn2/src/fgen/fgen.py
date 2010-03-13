#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

fgen.py

DFT SPL generator
"""

import sys
import getopt
import math
from factor import *

help_message = '''
This is the CS650 SPL compiler in PLY
    -h, --help              Displays this help message
    -v                      Sets the verbosity
    -n                      Sets the size of the DFT to be generated
    -o file, --output=file  The SPL output file
'''

def fgen(n, verbose=False):
	print isprime(n)
	print factors(n)
	print primefactors(n)

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:vn:", ["help", "output="])
		except getopt.error, msg:
			raise Usage(msg)
		
		verbose = False
		size = 32
		
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option == "-n":
				size = int(value)
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
	
	print verbose, size
	fgen(size, verbose)


if __name__ == "__main__":
	sys.exit(main())
