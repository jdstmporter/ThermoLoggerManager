import datetime
import json
from collections import defaultdict

import requests

WRITE_KEY = '8V5Q5QO2CO01B0BQ'
READ_KEY = '8V5Q5QO2CO01B0BQ'
channel_ID = "2818594"

class ThingSpeakRecord:



    def __init__(self,item):
        self.sequence = int(item['entry_id'])
        self.mac = item['field2']
        self.temperature = float(item['field3'])
        self.humidity = float(item['field4'])
        self.battery = float(item['field5'])
        self.ts = float(item['field7'])
        self.timestamp = datetime.datetime.fromtimestamp(self.ts)

    def __str__(self):
        return f'@ {self.timestamp}: T {self.temperature}C H {self.humidity}% B {self.battery}%'

    def sql(self):
        f"({self.sequence}, {self.ts}, {self.temperature}, {self.humidity}, {self.battery}, '{self.mac}')"


class ThingSpeakDownloader:
    MACS = {
        "c21200008b9d": 'Choir',
        "dc060000f29d": 'Kitchen',
        "fc0200008b9d": 'Organ',
        "690600008b9d": 'Pulpit',
        "ab0100008b9d": 'Lady Chapel',
        "260b0000f29d": 'TEST'
    }

    def __init__(self,params,payload):
        self.params=params
        self.payload=payload
        self.url = f'https://api.thingspeak.com/channels/{params.channel_ID}/feeds.json'

    def decode(self,data):
        try:
            items = defaultdict(list)
            records = data['feeds']
            for record in records:
                try:
                    item = ThingSpeakRecord(record)
                    if item.mac not in self.MACS:
                        raise RuntimeError(f'No location for MAC {item.mac}')
                    location = self.MACS[item.mac]
                    items[location].append(item)
                except Exception as e:
                    print(f'Error decoding record: {e}')
            return items
        except Exception as e:
            print(f'Error: {e}')
            return []



    def __call__(self):
        try:
            response = requests.get(self.url,params=self.payload)
            response.raise_for_status()
            data = response.json()
            return self.decode(data)
        except requests.exceptions.JSONDecodeError:
            raise RuntimeError('Badly formatted JSON')