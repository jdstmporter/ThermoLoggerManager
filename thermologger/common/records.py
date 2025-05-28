import datetime

from marshmallow.fields import Boolean

from .beacons import Beacons

def bool2int(b: bool) -> int :
    return 1 if b else 0

def int2bool(i: int) -> bool:
    return bool(i)

class Record:
    def __init__(self,*args):
        if len(args)==5:
            mac, temperature, humidity, battery, timestamp = args
            sensor=mac
            known=False
        elif len(args)==6:
            mac, sensor, temperature, humidity, battery, timestamp = args
            known=mac != sensor
        elif len(args)==7:
            mac, sensor, known, temperature, humidity, battery, timestamp = args
        else:
            raise RuntimeError(f'Bad record {args}')

        self.mac=str(mac)
        self.sensor=str(sensor)
        self.known=bool(known)
        self.temperature=temperature
        self.humidity=humidity
        self.battery=battery
        self.ts=timestamp
        self.timestamp = datetime.datetime.fromtimestamp(self.ts)

    def __str__(self):
        return f'{self.sensor} @ {self.timestamp}: T {self.temperature}C H {self.humidity}% B {self.battery}%'

    def sql(self,beacons):
        if self.mac in beacons:
            sensor=beacons[self.mac]
            return f"('{self.mac}', '{sensor.name}', 1, {int(self.ts)}, {self.temperature}, {self.humidity}, {self.battery})"
        else:
            return f"('{self.mac}', '{self.mac}', 0, {int(self.ts)}, {self.temperature}, {self.humidity}, {self.battery})"

    def dict(self):
        return {
            'mac' : self.mac,
            'sensor' : self.sensor,
            'known' : self.known,
            'timestamp' : self.ts,
            'temperature' : self.temperature,
            'humidity' : self.humidity,
            'battery' : self.battery
        }

