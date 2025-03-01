#!/usr/bin/env python3

import sched
import time


from thermologger.api import ScanForUpdates
from thermologger.db import SQLStore
from thermologger.common import Params

'''
    To read use

    https://api.thingspeak.com/channels/<CHANNEL_ID>/feeds.json?api_key=<READ_KEY>&ndays=<N>
'''




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
            print('Contacting SQL')
            try:
                things = SQLStore(self.params)
                things.write([b.record() for b in beacons])
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












