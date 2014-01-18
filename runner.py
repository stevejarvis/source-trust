#!/usr/local/bin/python3
"""
From the perspective of this exercise, .marshal files are binaries. Since
they aren't *really* binaries, they need a runner. This is the runner!
"""

import sys
import marshal

def run( obj ):
    """ Execute a given code object. """
    try:
        ret = exec( obj )
    except TypeError as e:
        print( 'Runner expected code object. Error: %s' %e )

def unmarshal( marshalpath ):
    """ Resolve a marshal'd object. """
    with open( marshalpath, 'rb' ) as f:
        obj = marshal.load( f )
    return obj


if __name__ == '__main__':
    if len( sys.argv ) < 2:
        print( 'Usage: runner.py <path to .marshal>' )
        sys.exit( 0 )

    obj = unmarshal( sys.argv[1] )
    run( obj )
