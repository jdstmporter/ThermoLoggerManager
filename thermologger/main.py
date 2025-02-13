#!/usr/bin/env python3
import os.path
import sched
import time
import json
import __main__

from thermologger.api import ScanForUpdates
from thermologger.things import ThingSpeak


class Params:

    def __init__(self,**kwargs):
        self.dict = dict(
            scan_time=60,
            wait_time=300,
            channel_ID = '2818594',
            url='https://api.thingspeak.com/channels/{channel_ID}/bulk_update.json',
            READ_KEY='8V5Q5QO2CO01B0BQ',
            WRITE_KEY='8V5Q5QO2CO01B0BQ',
            name='ThermoBeacon',
            response_length=18
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




class RunLoop:

    def __init__(self,config='config/config.json'):
        self.params = Params.load(config)
        self.scheduler = sched.scheduler(time.time, time.sleep)


    def action(self):
        scanner = ScanForUpdates(self.params)
        beacons = scanner.run()

        print(f'Got {len(beacons)} records')
        for beacon in beacons:
            print(str(beacon))

        # now do the thingspeak bit
        if len(beacons) > 0:
            print('Contacting ThingSpeak')
            try:
                things = ThingSpeak(self.params)
                things([b.dict() for b in beacons])
                print('Uploaded')
            except Exception as e:
                print(f'Error: {str(e)}')

    def runner(self):
        self.action()
        self.scheduler.enter(self.params.wait_time, 1, self.runner, ())

    def run(self):
        self.runner()
        try:
            self.scheduler.run()
        except KeyboardInterrupt:
            print('Exiting')












