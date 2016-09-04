#!/usr/bin/env python
#
#  This is the main application controller and management script.
#  This can be used to interface the application to a WSGI server, CGI, a
#  stand-alone server on 127.0.0.1:8080, or to create the database structure
#  and load test data.
#
#  NOTE: This file can probably be used without modification.
#
#  See the README.md for more information
#
#  Written by Sean Reifschneider <jafo@jafo.ca>, 2013
#
#  Part of the python-bottle-skeleton project at:
#
#      https://github.com/linsomniac/python-bottle-skeleton
#
#  I hereby place this work, python-bottle-wrapper, into the public domain.

import sys
import os
import website


if __name__.startswith('_mod_wsgi_'):
    os.chdir(os.path.dirname(__file__))
    sys.path.append('lib')
    sys.path.append('.')

    application = website.build_application()

if __name__ == '__main__':
    sys.path.append('lib')

    import model
    import bottle

    if os.environ.get('GATEWAY_INTERFACE'):
        #  Called from CGI
        app = website.build_application()
        bottle.run(app, server=bottle.CGIServer)
        sys.exit(0)

    if 'test-server' in sys.argv[1:]:
        'Run stand-alone test server'
        sys.path.append('tests')

        if os.environ.get('DBCREDENTIALSTR') == 'sqlite:///:memory:':
            model.initdb()
            model.create_sample_data()
        app = website.build_application()
        

        bottle.debug(True)
        bottle.run(app, reloader=True, host='127.0.0.1', port=8080)
        sys.exit(0)

    if 'initdb' in sys.argv[1:]:
        'Run database initialization'
        model.initdb()
        sys.exit(0)

    if 'load-test-data' in sys.argv[1:]:
        'Load test data-set'
        model.create_sample_data()
        sys.exit(0)
