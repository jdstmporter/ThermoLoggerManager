from collections import defaultdict
from http import HTTPStatus
from web.common import syslog, LogLevel
import re

class ResponseObject:
    def __init__(self, status=HTTPStatus.OK, contentType='text/plain', text=b'',headers=None):
        self.status = status
        self.headers = [('Content-type', contentType)]
        if headers is not None:
            self.headers.extend(headers)
        self.text = [text]

    def __call__(self,respond):
        try:
            syslog(LogLevel.INFO,f"Response: {self.status}")
            for h in self.headers:
                syslog(LogLevel.INFO,f'{h[0]},{h[1]}')
            s_txt = f'{self.status.value} {self.status.phrase}'
            respond(s_txt, self.headers)
        except Exception as e:
            syslog(LogLevel.CRITICAL,f"Error: {e}")
            respond(f'500 SERVER ERROR',self.headers)


class WSGIHeaders:
    def __init__(self):
        self._headers = defaultdict(set)

    def __len__(self):
        return len(self._headers)

    def __getitem__(self, item):
        return self._headers[item]

    def __setitem__(self, key, value):
        self._headers[key].add(value)

    def len(self,key):
        return len(self[key])

    def keys(self):
        return list(self._headers.keys())

    def __contains__(self, item):
        return item in self._headers

    def render(self):
        out = []
        for k in self.keys():
            out.extend([(k,v) for v in self[k]])
        return out



class WSGIEnvironment:
    def __init__(self):
        self.environ = {}
        self.headers = {}

    def load(self,environ):
        self.environ = environ
        headers={}
        for key in environ:
            matcher = re.match('^HTTP_([A-Z]+)$',key)
            if matcher is not None:
                try:
                    hdr = re.sub ('_','-',matcher[1]).lower().title()
                    headers[hdr]=environ[key]
                except:
                    syslog(LogLevel.DEBUG,f'Anomalous header {key}')
        self.headers=headers

    def header(self,key):
        return self.headers.get(key)

    def header_keys(self):
        return list(self.headers.keys())

    def method(self):
        return self.environ.get('REQUEST_METHOD')

