from datetime import datetime
from urllib.parse import parse_qs, urlparse
import json
from http import HTTPStatus
from thermologger.common import syslog, LogLevel

from thermologger.db import SQLStore

def asDate(lst,default=datetime.min):
    try:
        return datetime.fromtimestamp(float(lst[0]))
    except:
        return default

class ResponseObject:
    def __init__(self, status=HTTPStatus.OK, contentType='text/plain', text=b''):
        self.status = status
        self.headers = [('Content-type', contentType)]
        self.text = [text]

    def __call__(self,respond):
        s_txt = f'{self.status.value} {self.status.phrase}'
        respond(s_txt, self.headers)



class WSGIApp:

    def __init__(self, params):
        self.params=params
        self.sql = SQLStore(self.params)

    def _get_data(self,query,*args):
        try:
            args = parse_qs(query)
            start = asDate(args.get('s', []), default=datetime.min)
            end = asDate(args.get('e', []), default=datetime.max)
        except:
            start = datetime.min
            end = datetime.max

        records = self.sql.read()
        obj = [r.dict() for r in records]
        data = json.dumps(obj)

        return ResponseObject(contentType='application/json',
                              text=data.encode('utf-8'))

    def _get_schema(self,*args):
        return ResponseObject(contentType='application/json',
                              text=b'{}')

    def _get_beacons(self,*args):
        beacons = self.sql.beacons()
        data = json.dumps(beacons)
        return ResponseObject(contentType='application/json',
                              text=data.encode('utf-8'))


    def GET(self,path):
        parsed = urlparse(path)
        path = parsed.path
        if path == '/data':
            return self._get_data(parsed.query)
        elif path == '/schema':
            return self._get_schema()
        elif path == '/beacons':
            return self._get_beacons()
        else:
            return ResponseObject(status=HTTPStatus.NOT_FOUND)


    def PUT(self,path):
        return ResponseObject(text=b'ok')



    def __call__(self, environ, start_response):
        try:
            path = environ.get('PATH_INFO')
            method = environ.get('REQUEST_METHOD')
            if method == 'GET':
                responder = self.GET(path)
            elif method == 'PUT':
                responder = self.PUT(path)
            else:
                responder = ResponseObject(status=HTTPStatus.NOT_IMPLEMENTED)
        except Exception as e:
            syslog(LogLevel.ERROR,f'Error {type(e).__name__}: {e}')
            responder = ResponseObject(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        responder(start_response)
        return responder.text

