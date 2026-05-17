import json
import __main__
import os.path
from .loadable import KeyedDict



class Params(KeyedDict):

    def __init__(self,**kwargs):
        d = dict(
            scan_time=60,
            wait_time=300,
            scheduler_size=50,
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
            debugWeb=False,
            gc=False,
            meteo=dict(
                provider='MetOfficeProvider',
                latitude=51.90006,
                longitude=-2.07972,
                path='https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/hourly',
                apiKey='eyJ4NXQjUzI1NiI6Ik5XVTVZakUxTkRjeVl6a3hZbUl4TkdSaFpqSmpOV1l6T1dGaE9XWXpNMk0yTWpRek5USm1OVEE0TXpOaU9EaG1NVFJqWVdNellXUm1ZalUyTTJJeVpBPT0iLCJraWQiOiJnYXRld2F5X2NlcnRpZmljYXRlX2FsaWFzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ==.eyJzdWIiOiJqdWxpYW5AcG9ydGVybmV0Lm5ldEBjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6Imp1bGlhbkBwb3J0ZXJuZXQubmV0IiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJzaXRlX3NwZWNpZmljLTUwYzBhNGFlLTc1ZGUtNGZjZi1hZTQ2LWUxMWUzODZmMDA3MSIsImlkIjo0MzAzNCwidXVpZCI6IjY1YjM5ZDVkLTZjYzktNGU2NS1iZDNiLTA3YTUyYTQyZGY2NiJ9LCJpc3MiOiJodHRwczpcL1wvYXBpLW1hbmFnZXIuYXBpLW1hbmFnZW1lbnQubWV0b2ZmaWNlLmNsb3VkOjQ0M1wvb2F1dGgyXC90b2tlbiIsInRpZXJJbmZvIjp7IndkaF9zaXRlX3NwZWNpZmljX2ZyZWUiOnsidGllclF1b3RhVHlwZSI6InJlcXVlc3RDb3VudCIsImdyYXBoUUxNYXhDb21wbGV4aXR5IjowLCJncmFwaFFMTWF4RGVwdGgiOjAsInN0b3BPblF1b3RhUmVhY2giOnRydWUsInNwaWtlQXJyZXN0TGltaXQiOjAsInNwaWtlQXJyZXN0VW5pdCI6InNlYyJ9fSwia2V5dHlwZSI6IlBST0RVQ1RJT04iLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJTaXRlU3BlY2lmaWNGb3JlY2FzdCIsImNvbnRleHQiOiJcL3NpdGVzcGVjaWZpY1wvdjAiLCJwdWJsaXNoZXIiOiJKYWd1YXJfQ0kiLCJ2ZXJzaW9uIjoidjAiLCJzdWJzY3JpcHRpb25UaWVyIjoid2RoX3NpdGVfc3BlY2lmaWNfZnJlZSJ9XSwidG9rZW5fdHlwZSI6ImFwaUtleSIsImlhdCI6MTc3NDM2OTg4MSwianRpIjoiYmE4ZGY0NzQtZTIzMC00MjMxLWJhMzgtOGM0ZDkxMzMxNmU3In0=.fcCZWTbFFNirk9a_2j83QEN6kWlfixDdP5HBvlDejEmE2MvqOGG1i6mXzYsOhW32WUSajs38sn7ZTDHhypTpxc1edFUQWeBfW_HIZFsi6anMzZfYeuRFGXqdB9Mv8R9nfs9CRXSTCD-7tCj6obWWeEL4-FwoK_rFBC3i5EX9_wFSaAbCWtP_b9-Ndu5knzLQemuvbemSObJn44YfALaJXIAoV2v1uslTVMVQjs2ggIagJmG9I6Oah7CnMEJ4DGPz9pXzUDaIsWxFSHmlnqG0W4XoX7MtDX_zQJbUcG3Ph6KOSzNjiaSIVx26Wa211DldE16xdg0w3Q_7Z2bFZAg32w==',
                interval=3600
            )
        )
        d.update(kwargs)
        super().__init__(**d)

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

