import __main__
import os.path
import json
from .logs import syslog, LogLevel

class Loadable:
    @classmethod
    def _full_path(cls,path):
        if len(path) > 0 and path[0] == '/':
            return path
        else:
            if hasattr(__main__, '__file__'):
                main_file = __main__.__file__
                prefix = os.path.dirname(main_file)
                return os.path.join(prefix, path)
        raise Exception('no such path')

    @classmethod
    def load(cls, path):
        try:
            config=cls._full_path(path)
            print(f'Config path is {config}')
            with open(config, mode='r') as conf:
                j = json.load(conf)
        except Exception as e:
            syslog(LogLevel.ERROR,f'Error: {e}')
            j = dict()
        print('\n'.join([f'{key} = {value}' for key, value in j.items()]))
        return cls(**j)

    def __init__(self,**kwargs):
        self.dict=kwargs

class KeyedDict(Loadable):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def __getitem__(self, key):
        value = self.dict[str(key)]
        if type(value) == dict:
            return KeyedDict(**value)
        elif type(value) == list:
            d={ str(i) : value[i] for i in range(len(value)) }
            return KeyedDict(**d)
        else:
            return value

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __len__(self):
        return len(self.dict)

    def __contains__(self, key):
        return key in self.dict

    def keys(self):
        return self.dict.keys()

    def items(self):
        return self.dict.items()

    def __iter__(self):
        return iter(self.dict)