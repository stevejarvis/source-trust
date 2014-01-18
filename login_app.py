#!/usr/local/bin/python3
""" The login software. """

def login( password ):
    if password == 'please':
        print( 'Access Granted' )
    else:
        print( 'Access Denied' )


if len( sys.argv ) < 3:
    """ Assuming this will never be called without the runner. """
    print( 'Usage: login_app.py <password>' )
else:
    login( sys.argv[2] )
