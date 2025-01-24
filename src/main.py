#!/usr/bin/env python3

import sched
import time

from api import ScanForUpdates
from things import ThingSpeak

def action():
    scanner = ScanForUpdates(timeout=20)
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




if __name__=="__main__":
    PERIOD = 30
    scheduler = sched.scheduler(time.time,time.sleep)

    def run():
        action()
        scheduler.enter(PERIOD, 1, run, ())

    run()
    scheduler.run()




