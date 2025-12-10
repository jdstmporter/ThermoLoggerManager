from web.common import syslog, LogLevel
from .basehandlers import BaseHandler
from http import HTTPStatus
from urllib.parse import urlparse

class HEADERHandler(BaseHandler):
    def __init__(self,uri,cors=False,origin=None,routes=[]):
        super().__init__(uri,cors=cors,origin=origin,routes=routes)
        self.parsed=urlparse(self.uri)
        if self.cors:
            self.headers.append(('Access-Control-Allow-Origin',origin))

    def __call__(self):
        return self._response(data='')

    def schema(self):
       return ''

class GETHandler(HEADERHandler):

    def __call__(self):
        try:
            syslog(LogLevel.DEBUG,f'Full path is {self.parsed.path}')
            path=self.parsed.path[1:]
            syslog(LogLevel.DEBUG, f'Truncated path is {path}')
            if path in self.routes:
                action = getattr(self,path)
                data = action()
                return self._response(data=data)
            else:
                return self._error(HTTPStatus.FORBIDDEN)
        except Exception as e:
            syslog(LogLevel.ERROR,f'Bad request for ${self.uri} : ${e}')
            return self._error(HTTPStatus.BAD_REQUEST)


class OPTIONSHandler(BaseHandler):
    def __init__(self,uri,method='GET',origin=None):
        super().__init__(uri,origin=origin)
        self.method=method
        #self.cors_permitted = set()

    def __call__(self):
        if self.method == 'GET':
            extra_headers=[
                ('Access-Control-Allow-Methods', 'GET'),
                ('Access-Control-Allow-Headers', 'Content-Type, Accept'),
                ('Access-Control-Max-Age', '86400')
            ]
            if self.origin is not None:
                extra_headers.append(('Access-Control-Allow-Origin', self.origin))
            #self.cors_permitted.add(self.origin)
            self.headers.extend(extra_headers)
            return self._response(status=HTTPStatus.NO_CONTENT)
        else:
            return self._error(status=HTTPStatus.FORBIDDEN)
