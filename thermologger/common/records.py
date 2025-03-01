import datetime
from .beacons import beacon

class Record:
    def __init__(self,*args):
        if len(args)==5:
            mac, temperature, humidity, battery, timestamp = args
        else:
            raise RuntimeError(f'Bad record {args}')

        self.mac=beacon(str(mac))
        self.temperature=temperature
        self.humidity=humidity
        self.battery=battery
        self.ts=timestamp
        self.timestamp = datetime.datetime.fromtimestamp(self.ts)

    def __str__(self):
        return f'@ {self.timestamp}: T {self.temperature}C H {self.humidity}% B {self.battery}%'

    def sql(self):
        return f"({int(self.ts)}, {self.temperature}, {self.humidity}, {self.battery}, '{self.mac}')"

