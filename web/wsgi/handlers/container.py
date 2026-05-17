from collections import defaultdict
from http import HTTPMethod

from .basehandlers import BaseHandler
from .methodhandlers import OPTIONSHandler, HEADERHandler


class HandlerContainer:

    def __init__(self,**kwargs):
        self._methods = HTTPMethod.__members__.values()
        self._handlers = defaultdict(lambda : BaseHandler)
        for key, value in kwargs.items():
            if key.upper() in self._methods:
                self._handlers[key.upper()] = value


    def _getMethod(self,value):
        if type(value) == str:
            return value.upper()
        elif type(value) == HTTPMethod:
            return value.value
        else:
            return HTTPMethod.HEAD

    def __getitem__(self, item):
        if type(item) == str:
            return self._handlers[item]
        elif type(item) == HTTPMethod:
            return self._handlers[item.value]
        else:
            return BaseHandler

    def __setitem__(self, key, value):
        try:
            if type(key) == str and key.upper() in self._methods:
                self._handlers[key.upper()] = value
            elif type(key) == HTTPMethod:
                self._handlers[key.value] = value
        except:
            pass

    def extend(self,**kwargs):
        for k,v in kwargs:
            self[k]=v

    @classmethod
    def Load(cls,**kwargs):
        args = dict(
            OPTIONS = OPTIONSHandler,
            HEAD = HEADERHandler
        )
        args.update(kwargs)
        the = HandlerContainer(**args)

