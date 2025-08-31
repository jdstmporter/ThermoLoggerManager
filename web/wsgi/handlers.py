from collections import defaultdict

from thermologger.common import syslog, LogLevel
from urllib.parse import urlparse
from http import HTTPStatus, HTTPMethod
import re
from .protocol import ResponseObject


class URLManip:
    def __init__(self,url):
        self.url=url
        try:
            parse = re.match(r'^(http(s)?://)?([^:/]+)(:([0-9]+)?)?(.*)$',url)
            self.method, _, self.host, _, self.port, self.path = parse.groups()
        except:
            self.method = None
            self.host = None
            self.port = None
            self.path = None

class BaseHandler:
    def __init__(self,uri,cors=False,origin=None):
        self.uri=uri
        self.cors=cors
        self.origin=origin
        self.headers = []
        self.contentType='application/json'

    def _response(self,status=HTTPStatus.OK,data=''):
        return ResponseObject(status=status, contentType=self.contentType,
                              text=data.encode('utf-8'), headers=self.headers)

    def _error(self,status):
        return ResponseObject(status=status)

    def __call__(self):
        return self._error(HTTPStatus.NOT_FOUND)



class GETHandler(BaseHandler):
    def __init__(self,uri,cors=False,origin=None,routes=[]):
        super().__init__(uri,cors=cors,origin=origin)
        self.parsed=urlparse(self.uri)
        if self.cors:
            self.headers.append(('Access-Control-Allow-Origin',origin))
        self.routes=routes

    def __call__(self):
        try:
            path=self.parsed.path[1:]
            if path in self.routes:
                action = getattr(self,path[1:])
                data = action()
                return self._response(data=data)
            else:
                return self._error()
        except Exception as e:
            syslog(LogLevel.ERROR,f'Bad request for ${self.uri} : ${e}')
            return self._error(HTTPStatus.BAD_REQUEST)

    def schema(self):
       return ''

class HEADERHandler(BaseHandler):
    def __init__(self,uri,cors=False,origin=None):
        super().__init__(uri,cors=cors,origin=origin)
        self.parsed=urlparse(self.uri)
        if self.cors:
            self.headers.append(('Access-Control-Allow-Origin',origin))

    def __call__(self):
        return self._response(data='')

    def schema(self):
       return ''



class OPTIONSHandler(BaseHandler):
    def __init__(self,uri,method='GET',origin=None):
        super().__init__(uri,origin=origin)
        self.method=method
        #self.cors_permitted = set()

    def __call__(self):
        if self.method == 'GET':
            #self.cors_permitted.add(self.origin)
            self.headers.extend([
                ('Access-Control-Allow-Origin', self.origin),
                ('Access-Control-Allow-Methods', 'GET'),
                ('Access-Control-Allow-Headers', 'Content-Type, Accept'),
                ('Access-Control-Max-Age', '86400')
            ])
            return self._response(status=HTTPStatus.NO_CONTENT)
        else:
            return self._error(status=HTTPStatus.FORBIDDEN)


class HandlerContainer:

    def __init__(self):
        self._handlers = defaultdict(lambda : BaseHandler)
        self._methods = HTTPMethod.__members__.values()

    def _getMethod(self,value):
        if type(value) == str:
            return HTTPMethod.__members__.get(value.upper(),HTTPMethod.HEAD)
        elif type(value) == HTTPMethod:
            return value
        else:
            return HTTPMethod.HEAD

    def __getitem__(self, item : str|HTTPMethod):
        return self._handlers[self._getMethod(item)]

    def __setitem__(self, key, value):
        try:
            self._handlers[self._getMethod(key)]=value
        except:
            pass

    def __getattr__(self,item):
        return self[item]

    def extend(self,**kwargs):
        for k,v in kwargs:
            self[k]=v

    @classmethod
    def Load(cls,**kwargs):
        the = HandlerContainer()
        the[HTTPMethod.OPTIONS] = OPTIONSHandler
        the[HTTPMethod.HEAD] = HEADERHandler



