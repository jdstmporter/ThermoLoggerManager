import sched
import time


from thermologger.api import ScanForUpdates
from thermologger.db import SQLStore
from thermologger.common import Params, syslog, LogLevel




class RunLoop:

    def __init__(self,path,single_shot=False):
        self.params = Params.load(path)
        self.single_shot = single_shot
        self.scheduler = sched.scheduler(time.time, time.sleep)



    def action(self):
        scanner = ScanForUpdates(self.params)
        beacons = scanner.run()

        if syslog.isDebug:
            syslog(LogLevel.DEBUG,f'Got {len(beacons)} records')
            for beacon in beacons:
                syslog(LogLevel.DEBUG,str(beacon))

        if len(beacons) > 0:
            records = [b.record() for b in beacons]
            syslog(LogLevel.INFO,'Contacting SQL')
            try:
                things = SQLStore(self.params)
                things.write(records)
                syslog(LogLevel.INFO,'Uploaded')
            except Exception as e:

                syslog(LogLevel.ERROR,f'Error: {str(e)}')

    def runner(self):
        self.action()
        if not self.single_shot:
            self.scheduler.enter(self.params.wait_time, 1, self.runner, ())

    def run(self):
        self.runner()
        if not self.single_shot:
            try:
                self.scheduler.run()
            except KeyboardInterrupt:
                syslog(LogLevel.INFO,'Exiting')


