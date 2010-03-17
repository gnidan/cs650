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
from options import Options
from parser import SPLParser
from symbols import SymbolTable
import unparser

help_message = '''
This is the CS650 SPL compiler in PLY
    -h, --help              Displays this help message
    -i file, --input=file   The input file to be compiled
    -v                      Sets the verbosity
    -d                      Sets the debug flag
    -o file, --output=file  The output file
    -xposw, -xnegw          Sign of exponent in Nth root of unity
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv

    filename = None
    outfile = None
    verbose = False
    debug = False

    options = Options(unparser.C99())

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:vdx:o:", ["help", "input=", "output="])
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
                  options['sign'] = 1
              elif value == "negw":
                  options['sign'] = -1
              else:
                  raise Usage("Invalid option for -x\n\n" + help_message)
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-i", "--input"):
                filename = value
            if option in ("-o", "--output"):
                outfile = value

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

    out = sys.stdout
    if outfile is not None:
        out = open(outfile, 'w')

    if verbose: print "\n** Constructing the lexer and parser"
    parser = SPLParser(debug=debug)

    if verbose: print "\n** Initializing the symbol table"
    symtab = SymbolTable()

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

    if verbose:
        print "\n** Simplifying the AST (Constant Propagation, Defines)"
    t.simplify(symtab)
    if debug:
        print "\n Simplified AST:"
        print t
        print "\n Symbol Table Dump:"
        print symtab

    if verbose:
        print "\n** Translating the AST to icode"
    icodes = t.evaluate(symtab, options)

    #Get rid of the None's
    icodes = [i for i in icodes if i]
    if debug:
        print "\n Icodes:"
        print icodes

    if verbose:
        for i in icodes:
            print i.count()

    if verbose:
        print "\n** Optimization: Constant Propagation and Constant Folding (Pass #1)"
    for i in icodes:
        i.constprop()
        if debug:
            print "\nIcodes:"
            print i
        if verbose:
            print i.count()


    if verbose:
        print "\n** Processing: Inlining Calls"
    for i in icodes:
        i.inline_calls()

    if verbose:
        print "\n** Optimization: Unrolling the icode"
    for i in icodes:
        i.unroll()
        if debug:
            print "\nIcodes:"
            print i
        if verbose:
            print i.count()

    if verbose:
        print "\n** Optimization: Constant Propagation and Constant Folding (Pass #2)"
    for i in icodes:
        i.constprop()
        if verbose:
            print i.count()

    #if verbose:
    #    print "\n** Optimization: Subexpression elimination"
    #for i in icodes:
    #    i.subexpr()

    if debug:
        print "\nIcodes:"
        print icodes

    if verbose:
        print "\n** Unparsing to %s" % (options.unparser.__class__.__name__)

    funcs = [ options.unparser.write_function(options, i) for i in icodes ]

    if outfile:
        print "Functions printed to %s" % (outfile)
    for f in funcs:
        print >> out, f

if __name__ == "__main__":
    sys.exit(main())
