#!/usr/bin/env python3
from thermologger.common import Params
from web.wsgi import WSGIApp
from wsgiref.simple_server import make_server

def server(config = 'config/config.json'):
    params = Params.load(config)

    print('Starting server')
    app = WSGIApp(params)

    ip=params.web_ip
    port=params.web_port
    print(f'Serving on port {ip}:{port}')
    httpd = make_server(ip, port, app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Interrupt')
        httpd.server_close()





