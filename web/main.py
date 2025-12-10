#!/usr/bin/env python3
from .common import Params, syslog, LogLevel, CmdLineArgs
from .wsgi import WSGIApplication, SafeWSGIServer

config_live='/etc/thermologger/config.json'
config_dev='config/config.json'

def run_safe(config: str):
    app = WSGIApplication(config)
    ip = app.parameters.web_ip
    port = app.parameters.web_port
    syslog(LogLevel.INFO, f'Serving on port {ip}:{port}')
    httpd = SafeWSGIServer(ip, port, app())
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        syslog(LogLevel.INFO, 'Interrupt: exiting')
        httpd.server_close()

def run(args):
    try:
        parser = CmdLineArgs()
        if parser(args):
            syslog.set_level(parser.log_level)
            run_safe(config_live if parser.is_live else config_dev)
        return 0
    except Exception as e:
        print(f'General error: {e}')

