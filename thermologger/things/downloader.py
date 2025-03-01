
from collections import defaultdict
import requests

from thermologger.common import Record

WRITE_KEY = '8V5Q5QO2CO01B0BQ'
READ_KEY = '8V5Q5QO2CO01B0BQ'
channel_ID = "2818594"



class ThingSpeakRecord(Record):
    def __init__(self,item):
        super().__init__(
                         item['field2'],
                         float(item['field3']),
                         float(item['field4']),
                         float(item['field5']),
                         float(item['field7']))





class ThingSpeakDownloader:


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
                    items[item.mac].append(item)
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