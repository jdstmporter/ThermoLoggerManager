#!/usr/bin/env python3
from web.common import Params, syslog, LogLevel, CmdLineArgs
from web.wsgi import WSGIApp, SafeWSGIServer

config_live='/etc/thermologger/config.json'
config_dev='config/config.json'


def server(config = 'config/config.json'):
    params = Params.load(config)

    syslog(LogLevel.INFO,'Starting server')
    app = WSGIApp(params)

    ip=params.web_ip
    port=params.web_port
    syslog(LogLevel.INFO,f'Serving on port {ip}:{port}')
    httpd = SafeWSGIServer(ip, port, app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        syslog(LogLevel.INFO,'Interrupt: exiting')
        httpd.server_close()



def run(args):
    try:
        parser = CmdLineArgs()
        if parser(args):
            syslog.set_level(parser.log_level)
            server(config_live if parser.is_live else config_dev)
        return 0
    except Exception as e:
        print(f'General error: {e}')

