from .handlers.methodhandlers import HEADERHandler
from .protocol import WSGIEnvironment, ResponseObject
from .handlers import OPTIONSHandler, GETHandler, URLManip, HandlerContainer
from datetime import datetime
from http import HTTPStatus, HTTPMethod
from urllib.parse import parse_qs
import json
from web.common import syslog, LogLevel
from web.db import SQLStore

def asDate(lst,default=datetime.min):
    try:
        return datetime.fromtimestamp(float(lst[0]))
    except:
        return default


class WSGIApp:

    keys = [
        'PATH_INFO',
        'REQUEST_METHOD',
        'HTTP_ORIGIN',
        'HTTP_REFERER',
        'HTTP_HOST',
        'HTTP_ACCEPT',
        'HTTP_ACCESS_CONTROL_REQUEST_METHOD',
        'HTTP_SEC_FETCH_MODE',
        'HTTP_SEC_FETCH_DEST',
        'HTTP_SEC_FETCH_SITE'
    ]

    def __init__(self, params, handlers = HandlerContainer.Load()):
        self.params=params
        self.sql = SQLStore(self.params)
        self.origin_Port = params.static_port
        self.dynamic_port = params.web_port
        self.cors_permitted = set()
        self.headers = WSGIEnvironment()
        self.debug = params.debugWeb
        self.handlers = handlers

    def __call__(self, environ, start_response):

        try:
            self.headers.load(environ)
            if self.debug:
                self._debug(WSGIApp.keys,environ)

            path = environ.get('PATH_INFO')
            method = environ.get('REQUEST_METHOD')
            cors = environ.get('HTTP_SEC_FETCH_MODE') is not None
            origin = environ.get('HTTP_ORIGIN')
            if origin is None:
                origin = environ.get('HTTP_REFERER')
            requested_method = environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
            responder=self.handlers[method](path,origin=origin,cors=cors,method=requested_method,sql=self.sql)()
        except Exception as e:
            syslog(LogLevel.CRITICAL,f'Error {type(e).__name__}: {e}')
            responder = ResponseObject(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        responder(start_response)
        return responder.text

    def _debug(self,keys,environ):
        syslog(LogLevel.INFO, "Environment dictionary")
        for k in keys:
            syslog(LogLevel.INFO, f'{k} : {environ.get(k)}')

        syslog(LogLevel.INFO, 'Headers')
        for k in self.headers.header_keys():
            syslog(LogLevel.INFO, f'{k} : {self.headers.header(k)}')
        origin_port = URLManip(self.headers.header('Origin')).port
        wsgi_port = URLManip(self.headers.header('Host')).port
        syslog(LogLevel.INFO, f'STATIC {origin_port}, DYNAMIC {wsgi_port}')


