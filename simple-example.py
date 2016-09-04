#!/usr/bin/env python
#
#  This is about the simplest Bottle app you can make.
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

def website():
    app = bottle.Bottle()

    bottle.BaseTemplate.defaults['app'] = app
    bottle.TEMPLATE_PATH.insert(0, 'views')

    #  a couple index URL aliases so the main page renders
    @app.route('/', name='user_list')
    @app.route('/', name='user_new')

    @app.route('/', name='index')    #  XXX Location of page
    @bottle.view('index')            #  XXX Template to use
    def index():
        #  XXX Page code here

        import datetime

        now = datetime.datetime.now()

        #  XXX Return variables for use in page rendering
        return {'now': now}

    return app

#  interfaces to various web servers
import os
import sys
sys.path.append('lib')

#  called from a WSGI server
if __name__.startswith('_mod_wsgi_'):
    os.chdir(os.path.dirname(__file__))
    import bottle
    application = website()

if __name__ == '__main__':
    import bottle

    app = website()

    #  called as a CGI
    if os.environ.get('GATEWAY_INTERFACE'):
        bottle.run(app, server=bottle.CGIServer)
        sys.exit(0)

    #  standalone server
    app = website()
    bottle.run(app, reloader=True, host='127.0.0.1', port=8080)
