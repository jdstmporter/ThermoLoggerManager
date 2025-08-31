from collections import defaultdict
from http import HTTPMethod

from .basehandlers import BaseHandler
from .methodhandlers import OPTIONSHandler, HEADERHandler


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

