import requests
from datetime import datetime

class GeographicLocation:

    def __init__(self,latitude : float, longitude : float):
        self.latitude=latitude
        self.longitude=longitude

    @property
    def latitudeNS(self):
        suffix = 'N' if self.latitude>=0 else 'S'
        return f'{abs(self.latitude)}{suffix}'

    @property
    def longitudeEW(self):
        suffix = 'E' if self.longitude >= 0 else 'W'
        return f'{abs(self.longitude)}{suffix}'


    def __str__(self):
        return f'{self.latitudeNS}, {self.longitudeEW}'

class JSONObject:
    def __init__(self,data):
        self.json=data

    def _valueFrom(self,value):
        if type(value) in [list, dict]:
            return JSONObject(value)
        else:
            return value

    def __len__(self):
        return len(self.json)

    def __getitem__(self,idx):
        #print(f'Index {idx}')
        if type(self.json)==list:
            return self._valueFrom(self.json[idx])
        else:
            raise Exception(f'JSON: not a list')

    def __getattr__(self,key : str):
        #print(f'Key {key}')
        if type(self.json)==dict:
            return self._valueFrom(self.json[key])
        else:
            raise Exception(f'JSON: not a dictionary')

class MeteorologyDatum:
    def __init__(self,time,temperature,humidity):
        self.timestamp = datetime.fromisoformat(time).timestamp()
        self.temperature = temperature
        self.humidity = humidity

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

    def __str__(self):
        items = [f'{self.datetime}', f'{self.temperature}C']
        if self.humidity is not None:
            items.append(f'{self.humidity}%')
        return ' '.join(items)

    def dict(self):
        return dict(timestamp=self.timestamp,temperature=self.temperature,humidity=self.humidity)

class BaseMeteorologyData:
    def __init__(self,dat : dict):
        self.json=JSONObject(dat)
        self.items=[]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]

    def __iter__(self):
        return iter(self.items)


class BaseMeteorologyProvider:

    def __init__(self,centre: GeographicLocation):
        self.centre=centre

    def url(self):
        return ''

    def attributes(self):
        return dict()

    def headers(self):
        return dict()

    def __call__(self):
        response = requests.request('GET', self.url(), params=self.attributes(), headers=self.headers())
        response.raise_for_status()
        return response.json()













