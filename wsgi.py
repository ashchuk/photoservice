#!/usr/bin/env python
import importlib.machinery

if __name__ == '__main__':
    print('Executing __main__ ...')
    ip = 'localhost'
    port = 8051
    app = importlib.machinery.SourceFileLoader("application", 'wsgi/application').load_module("application")

    from wsgiref.simple_server import make_server
    httpd = make_server(ip, port, app.application)
    print('Starting server on http://{0}:{1}'.format(ip, port))
    httpd.serve_forever()
