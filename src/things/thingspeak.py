import json
import requests

class ThingSpeakException(Exception):
    def __init__(self,status):
        super().__init__()
        self.status=status

    def __str__(self):
        return f'ThingSpeak error : {self.status}'

WRITE_KEY = '8V5Q5QO2CO01B0BQ'
READ_KEY = '8V5Q5QO2CO01B0BQ'
channel_ID = "2818594"

class ThingSpeak:


    def __init__(self):
        self.url = f'https://api.thingspeak.com/channels/{channel_ID}/bulk_update.json'
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'THINGSPEAKAPIKEY': WRITE_KEY
        }


    def __call__(self,records=[]):
        try:
            record = dict(
                write_api_key = WRITE_KEY,
                updates = records
            )
            j = json.dumps(record)
            self.headers['Content-Length']=str(len(j))
            print(f'Logging {j} to {self.url}')
            response = requests.post(self.url, headers=self.headers,data=j)
            if response.status_code not in [200,201,202]:
                raise ThingSpeakException(f'HTTP {response.status_code} {response.reason}')
            return response.json()
        except ThingSpeakException as e:
            print(str(e))
            raise e
        except Exception as e:
            raise ThingSpeakException(str(e))