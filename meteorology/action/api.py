import requests
from datetime import datetime
from thermologger.common import KeyedDict


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



class MeteorologyDatum:
    def __init__(self,time,temperature,humidity):
        if type(time)==str:
            self.timestamp = datetime.fromisoformat(time).timestamp()
        else:
            self.timestamp = time
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

    def sql(self):
        return f"('{int(self.timestamp)}', {self.temperature}, {self.humidity})"

    def dict(self):
        return dict(timestamp=self.timestamp,temperature=self.temperature,humidity=self.humidity)

class BaseMeteorologyData:
    def __init__(self,dat : dict):
        self.json=KeyedDict(**dat)
        self.items=[]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]

    def __iter__(self):
        return iter(self.items)









