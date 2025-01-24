#!/usr/bin/env python3

import sched
import time

from api import ScanForUpdates
from things import ThingSpeak

class RunLoop:

    def __init__(self,scan_time=20,wait_time=300):
        self.scan_time=scan_time
        self.wait_time=wait_time
        self.scheduler = sched.scheduler(time.time, time.sleep)


    def action(self):
        scanner = ScanForUpdates(timeout=self.scan_time)
        beacons = scanner.run()

        print(f'Got {len(beacons)} records')
        for beacon in beacons:
            print(str(beacon))

        # now do the thingspeak bit
        if len(beacons) > 0:
            print('Contacting ThingSpeak')
            try:
                things = ThingSpeak()
                things([b.dict() for b in beacons])
                print('Uploaded')
            except Exception as e:
                print(f'Error: {str(e)}')

    def runner(self):
        self.action()
        self.scheduler.enter(self.wait_time, 1, self.runner, ())

    def run(self):
        self.runner()
        self.scheduler.run()











