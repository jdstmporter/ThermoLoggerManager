import requests

from meteorology.action.api import GeographicLocation


class BaseMeteorologyProvider:
    _registry = dict()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseMeteorologyProvider._registry[cls.__name__]=cls

    @classmethod
    def Load(cls,name):
        try:
            return cls._registry[name]
        except Exception as e:
            raise Exception(f'Cannot load {name} : error {e}')

    @classmethod
    def dataStructure(cls,json_data):
        return json_data

    def __init__(self,centre: GeographicLocation,path: str,apikey: str):
        self.centre=centre
        self.url = path
        self.apikey = apikey

    def attributes(self):
        return dict()

    def headers(self):
        return dict()

    def __call__(self):
        response = requests.request('GET', self.url, params=self.attributes(), headers=self.headers())
        response.raise_for_status()
        #json.dumps(response.json(),indent=2)
        return self.__class__.dataStructure(response.json())






