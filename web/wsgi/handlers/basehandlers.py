from collections import defaultdict

from thermologger.common import syslog, LogLevel
from urllib.parse import urlparse
from http import HTTPStatus, HTTPMethod
import re
from web.wsgi.protocol import ResponseObject


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
    def __init__(self,uri,cors=False,origin=None,routes=[]):
        self.uri=uri
        self.cors=cors
        self.origin=origin
        self.headers = []
        self.contentType='application/json'
        self.routes=routes

    def _response(self,status=HTTPStatus.OK,data=''):
        return ResponseObject(status=status, contentType=self.contentType,
                              text=data.encode('utf-8'), headers=self.headers)

    def _error(self,status):
        return ResponseObject(status=status)

    def __call__(self):
        return self._error(HTTPStatus.NOT_FOUND)






