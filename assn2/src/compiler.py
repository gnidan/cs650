#!/usr/bin/env python
# encoding: utf-8
"""
CS650
Kevin Lynch
Nick D'Andrea
Keith Dailey

compiler.py

PLY SPL compiler.

"""

import sys
import getopt

from parser import SPLParser

help_message = '''
This is the CS650 SPL compiler in PLY
    -h, --help              Displays this help message
    -i file, --input=file   The input file to be compiled
    -v                      Sets the verbosity
    -xposw, -xnegw          Sign of exponent in Nth root of unity
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv

    filename = None
    verbose = False
    debug = False
    sign = 1

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:vdx:", ["help", "input="])
        except getopt.error, msg:
            raise Usage(msg)

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option == "-d":
                debug = 1
            if option == "-x":
              if value == "posw":
                  sign = 1
              elif value == "negw":
                  sign = -1
              else:
                  raise Usage("Invalid option for -x\n\n" + help_message)
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-i", "--input"):
                filename = value

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

    if filename is None:
        sys.stdout.write("Reading from standard input (type EOF to end):\n")
        data = sys.stdin.read()
    else:
        f = open(filename)
        data = f.read()
        f.close()

    if verbose: print "\n** Constructing the lexer and parser"
    parser = SPLParser(debug=debug)

    if verbose:	print "\n** Constructing the AST"
    try:
        t = parser.parse(data)
    except Exception, err:
        print err
        raise
        return 2

    if verbose:
        print "\n** Printing the AST"
        print t

    if t is None:
        return


#if verbose: print "\n** Initializing the Environment"
#env = runtime.Environment(debug=debug)

#if verbose: print "\n** Evaluating the AST"
#try:
#	print t.evaluate(env)
#except runtime.RuntimeException, e:
#	print e

#if verbose:
#	print "\n** Dumping the Environment"
#	print env

if __name__ == "__main__":
    sys.exit(main())