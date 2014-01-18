#!/usr/local/bin/python3
"""
The compiler is really the code object on disk as compiler.marshal, and this is
the source used to generate that "binary".
"""

import marshal
import sys
import inspect


def build( inPath, outPath ):
    print( 'Building %s...' %inPath )
    with open( inPath, 'r' ) as f:
        source = ''
        for line in f.readlines():
            source += line
    co = compile( source, inPath, 'exec' )
    with open( outPath, 'wb' ) as f:
        marshal.dump( co, f )
    print( 'Done' )

def getOutputFile( inPath ):
    return inPath[:-3] + '.marshal'

def printUsage():
    print( 'Usage: compiler.py input' )


""" Need to know if called indirectly through the marshal'd object. """
caller = inspect.stack()
if len( caller ) == 1:
    """ Assume called directly. """
    if len( sys.argv ) < 2:
        printUsage()
    else:
        build( sys.argv[1], getOutputFile( sys.argv[1] ) )
else:
    """ Assume called via runner.py """
    if len( sys.argv ) < 3:
        """ Because executed from runner.py, arg to compiler will actually be
        third element. If running something else, ignore the complaining. """
        printUsage()
    else:
        build( sys.argv[2], getOutputFile( sys.argv[2] ) )
