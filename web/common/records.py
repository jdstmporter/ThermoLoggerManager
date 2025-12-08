import datetime


MACS = {
    "c21200008b9d": 'Choir',
    "dc060000f29d": 'Kitchen',
    "fc0200008b9d": 'Organ',
    "690600008b9d": 'Pulpit',
    "ab0100008b9d": 'Lady Chapel',
    "260b0000f29d": 'TEST',
    "610400008c6c": 'NEW 1',
    "880400008c6c": 'NEW 2'
}

class Beacons:

    def __init__(self,raw={}):
        self.beacons=raw

    def __getitem__(self,mac):
        return self.beacons.get(mac,mac)


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
        sensor = beacons.get(self.sensor,self.mac)
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

