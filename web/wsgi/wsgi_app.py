from handlers import HandlerContainer
from server import TempGETHandler
from web.common import Params, syslog, LogLevel
from .server import WSGIApp
from .httpd import SafeWSGIServer

class WSGIApplication:
    def __init__(self,config : str, handlers : HandlerContainer):
        self._params = Params.load(config)
        self._handlers = handlers


    def __call__(self) -> WSGIApp:
        syslog(LogLevel.INFO, 'Starting server')
        return WSGIApp(self._params,self._handlers)

    @property
    def parameters(self) -> Params:
        return self._params

    @classmethod
    def load(cls,config : str, handlers: HandlerContainer) -> WSGIApp:
        wsgi = WSGIApplication(config,handlers)
        return wsgi()

