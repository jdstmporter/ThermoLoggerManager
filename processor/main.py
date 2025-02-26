
from common import Params
from processor.thingspeak import ThingSpeakDownloader


def run(args):
    params = Params.load('config/config.json')
    payload = {'api_key': params.READ_KEY}
    if hasattr(args, 'count'):
        payload['results'] = min(args.count, 8000)
    elif hasattr(args, 'days'):
        payload['days'] = args.days
    else:
        payload['days'] = params.ndays
    downloader = ThingSpeakDownloader(params,payload)
    out = downloader()
    for key in out.keys():
        print(str(key))
        for item  in out[key]:
            print(f'    {item}')
