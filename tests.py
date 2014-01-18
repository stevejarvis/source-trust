#!/usr/local/bin/python3
"""
Even fun things deserve tests.
"""

import unittest
import marshal
import os
import ast
import glob

import runner
import compiler


def functionTouchFile():
    with open( 'test.test', 'w' ) as f:
        f.write( 'Test was here' )


class Test( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        for f in glob.glob( '*.test' ):
            os.remove( f )

    def testUnpickling( self ):
        d = { 'somekey' : 1,
              'foobaz' : 34,
              'bla' : 'hi' }
        with open( 'marshal.test', 'wb' ) as f:
            marshal.dump( d, f )
        dd = runner.unmarshal( 'marshal.test' )
        self.assertDictEqual( d, dd, "Dictionaries differ!" )

    def testRunner( self ):
        co = functionTouchFile.__code__
        ret = runner.run( co )
        try:
            with open( 'test.test', 'r'):
                pass
        except IOError:
            self.assertTrue( False, 'Code object file not made.' )

    def testOutfileGeneration( self ):
        fname = 'compiler.py'
        self.assertEqual( compiler.getOutputFile( fname ),
                          'compiler.marshal',
                          'Bad slice' )

    def testCompiler( self ):
        compiler.build( 'compiler.py', 'compiler.test' )
        try:
            with open( 'compiler.test', 'r'):
                pass
        except IOError:
            self.assertTrue( False, 'Compiled marshal not made.' )


if __name__ == '__main__':
    unittest.main()
