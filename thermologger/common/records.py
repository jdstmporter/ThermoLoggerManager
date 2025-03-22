import datetime
from .beacons import Beacons

class Record:
    def __init__(self,*args):
        if len(args)==5:
            mac, temperature, humidity, battery, timestamp = args
            sensor=mac
        elif len(args)==6:
            mac, sensor, temperature, humidity, battery, timestamp = args
        else:
            raise RuntimeError(f'Bad record {args}')

        self.mac=str(mac)
        self.sensor=str(sensor)
        self.temperature=temperature
        self.humidity=humidity
        self.battery=battery
        self.ts=timestamp
        self.timestamp = datetime.datetime.fromtimestamp(self.ts)

    def __str__(self):
        return f'{self.sensor} @ {self.timestamp}: T {self.temperature}C H {self.humidity}% B {self.battery}%'

    def sql(self,beacons):
        sensor = beacons[self.sensor]
        return f"('{self.mac}', '{sensor}', {int(self.ts)}, {self.temperature}, {self.humidity}, {self.battery})"

    def dict(self):
        return {
            'mac' : self.mac,
            'sensor' : self.sensor,
            'timestamp' : self.ts,
            'temperature' : self.temperature,
            'humidity' : self.humidity,
            'battery' : self.battery
        }

