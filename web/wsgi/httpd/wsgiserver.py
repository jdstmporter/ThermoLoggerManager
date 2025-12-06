
from wsgiref.simple_server import make_server, WSGIServer
from wsgiref.simple_server import WSGIRequestHandler
from web.common import syslog, LogLevel


class SafeWSGIRequestHandler(WSGIRequestHandler):
    def handle(self):
        try:
            super().handle()
        except Exception as e:
            syslog(LogLevel.WARNING,f'Client Error: {e}')


def SafeWSGIServer(ip: str, port: int, app):
    return make_server(ip, port, app, WSGIServer, SafeWSGIRequestHandler)