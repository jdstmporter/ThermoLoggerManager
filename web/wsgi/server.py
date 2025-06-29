from .protocol import WSGIEnvironment, ResponseObject
from .handlers import URLManip, OPTIONSHandler, GETHandler
from datetime import datetime
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse
import json
from thermologger.common import syslog, LogLevel

from thermologger.db import SQLStore

def asDate(lst,default=datetime.min):
    try:
        return datetime.fromtimestamp(float(lst[0]))
    except:
        return default

class TempGETHandler(GETHandler):

    def __init__(self,path,sql,origin=None,cors=False):
        super().__init__(path,cors=cors,origin=origin)
        self.sql=sql

    def data(self):
        try:
            args = parse_qs(self.parsed.query)
            start = asDate(args.get('s', []), default=datetime.min)
            end = asDate(args.get('e', []), default=datetime.max)
        except:
            start = datetime.min
            end = datetime.max

        records = self.sql.read()
        obj = [r.dict() for r in records]
        return json.dumps(obj)

    def beacons(self):
        beacons = self.sql.beacons()
        return json.dumps(beacons)

    def range(self):
        (ma, mi) = self.sql.time_range()
        return json.dumps({'start': mi, 'end': ma})


class WSGIApp:

    handlers = dict(GET=TempGETHandler)

    def __init__(self, params):
        self.params=params
        self.sql = SQLStore(self.params)
        self.origin_Port = params.static_port
        self.dynamic_port = params.web_port
        self.cors_permitted = set()
        self.headers = WSGIEnvironment()

    def __call__(self, environ, start_response):
        keys = [
                'PATH_INFO',
                'REQUEST_METHOD',
                'HTTP_ORIGIN',
                'HTTP_HOST',
                'HTTP_ACCEPT',
                'HTTP_ACCESS_CONTROL_REQUEST_METHOD',
                'HTTP_SEC_FETCH_MODE',
                'HTTP_SEC_FETCH_DEST',
                'HTTP_SEC_FETCH_SITE'
            ]
        try:
            '''
            syslog(LogLevel.INFO,"Environment dictionary")
            for k in keys:
                syslog(LogLevel.INFO,f'{k} : {environ.get(k)}')
            self.headers.load(environ)
            syslog(LogLevel.INFO,'Headers')
            for k in self.headers.header_keys():
                syslog(LogLevel.INFO,f'{k} : {self.headers.header(k)}')
            origin_port = URLManip(self.headers.header('Origin')).port
            wsgi_port = URLManip(self.headers.header('Host')).port
            syslog(LogLevel.INFO, f'STATIC {origin_port}, DYNAMIC {wsgi_port}')
'''
            path = environ.get('PATH_INFO')
            origin = environ.get('HTTP_ORIGIN')
            method = environ.get('REQUEST_METHOD')
            if method == 'GET':
                cors = environ.get('HTTP_SEC_FETCH_MODE') is not None
                responder = self.handlers['GET'](path,origin=origin,cors=cors,sql=self.sql)()
            elif method == 'OPTIONS':
                requested_method=environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
                responder = OPTIONSHandler(path,method=requested_method,origin=origin)()
            else:
                responder = ResponseObject(status=HTTPStatus.NOT_IMPLEMENTED)
        except Exception as e:
            syslog(LogLevel.ERROR,f'Error {type(e).__name__}: {e}')
            responder = ResponseObject(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        responder(start_response)
        return responder.text

