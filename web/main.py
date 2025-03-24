#!/usr/bin/env python3
from thermologger.common import Params, syslog, LogLevel
from web.wsgi import WSGIApp
from wsgiref.simple_server import make_server

def server(config = 'config/config.json'):
    params = Params.load(config)

    syslog(LogLevel.INFO,'Starting server')
    app = WSGIApp(params)

    ip=params.web_ip
    port=params.web_port
    syslog(LogLevel.INFO,f'Serving on port {ip}:{port}')
    httpd = make_server(ip, port, app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        syslog(LogLevel.INFO,'Interrupt: exiting')
        httpd.server_close()





