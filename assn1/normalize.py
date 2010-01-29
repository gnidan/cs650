#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Kevin Lynch on 2010-01-28.
Copyright (c) 2010 Kevin Lynch. All rights reserved.
"""

import sys
import getopt
import copy

help_message = '''
Parses and normalizes the timing file into separate files for each function.
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:i:n:", ["help", "outext=","infile=", "normalize="])
		except getopt.error, msg:
			raise Usage(msg)
	
		infile = 'timings.txt'
		function = 'fftw_measure'
		outext = '.dat'
	
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--outext"):
				outext = value
			if option in ("-i", "--infile"):
				infile = value
			if option in ("-n", "--normalize"):
				normalize = True
				function = value
				
		data = {}
		for line in open(infile,'r'):
			values = line.split()
			f = values[0]
			k = int(values[1])
			vals = map(float, values[2:])
			if f not in data:
			 	data[f] = {}
			data[f][k] = vals

		if normalize:
			outext = '_norm' + outext			
			df = copy.deepcopy(data[f])
			for func in data:
				for k in data[func]:
					for i in xrange(len(data[func][k])):
						if df[k][i] == 0.0:
							df[k][i] = 0.0000000000001
						data[func][k][i] = data[func][k][i]/df[k][i]
						
		for func in data:
			outfile = open(func + outext, 'w')
			for k in data[func]:
				print >>outfile, func, k, 
				for v in data[func][k]:
					print >>outfile, v,
				print >>outfile
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
