import json
import __main__
import os.path
from .loadable import Loadable

class Params(Loadable):

    def __init__(self,**kwargs):
        d = dict(
            scan_time=60,
            wait_time=300,
            channel_ID = '2818594',
            url='https://api.thingspeak.com/channels/{channel_ID}/bulk_update.json',
            READ_KEY='8V5Q5QO2CO01B0BQ',
            WRITE_KEY='8V5Q5QO2CO01B0BQ',
            name='ThermoBeacon',
            response_length=18,
            db_database='AllSaints',
            db_host='localhost',
            db_user='sql',
            db_password='sql',
            db_port=3306,
            web_ip='0.0.0.0',
            web_port=8080,
            debugWeb=False
        )
        d.update(kwargs)
        super().__init__(**d)

    def __getitem__(self,key: str):
        return self.dict[key]

    def __getattr__(self, key: str):
        return self.dict[key]

    def __str__(self):
        lines = [ f'{key} = {value}' for key,value in self.dict.items()]
        return '\n'.join(lines)

'''
    @classmethod
    def load(cls,config):
        try:
            if hasattr(__main__,'__file__'):
                main_file = __main__.__file__
                prefix = os.path.dirname(main_file)
                config = os.path.join(prefix,config)
            #print(f'Config is now {config}')
            with open(config, mode='r') as conf:
                j = json.load(conf)
        except Exception as e:
            print(f'Error: {e}')
            j = dict()
        print('\n'.join([f'{key} = {value}' for key, value in j.items()]))
        return Params(**j)
'''

