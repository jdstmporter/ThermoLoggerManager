from web.common import Params, syslog, LogLevel
from .server import WSGIApp
from .httpd import SafeWSGIServer

class WSGIApplication:
    def __init__(self,config : str):
        self._params = Params.load(config)


    def __call__(self):
        syslog(LogLevel.INFO, 'Starting server')
        return WSGIApp(self._params)

    @property
    def parameters(self):
        return self._params


