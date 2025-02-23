
import os.path
import json
import __main__

from processor.thingspeak.things import ThingSpeakDownloader


class Params:

    def __init__(self,**kwargs):
        self.dict = dict(
            channel_ID = '2818594',
            url='https://api.thingspeak.com/channels/{channel_ID}/feeds.json',
            READ_KEY='8V5Q5QO2CO01B0BQ',
            WRITE_KEY='8V5Q5QO2CO01B0BQ',
            ndays=2
        )
        self.dict.update(kwargs)

    def __getitem__(self,key: str):
        return self.dict[key]

    def __getattr__(self, key: str):
        return self.dict[key]

    def __str__(self):
        lines = [ f'{key} = {value}' for key,value in self.dict.items()]
        return '\n'.join(lines)

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

def run():
    params = Params.load('config/config.json')
    downloader = ThingSpeakDownloader(params)
    out = downloader()
    for key in out.keys():
        print(str(key))
        for item  in out[key]:
            print(f'    {item}')
