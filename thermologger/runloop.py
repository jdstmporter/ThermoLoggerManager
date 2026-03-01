import gc

from thermologger.api import ScanForUpdates
from thermologger.common.schedule import SimpleScheduler
from thermologger.db import SQLStore
from thermologger.common import Params, syslog, LogLevel




class RunLoop:

    def __init__(self,path,single_shot=False):
        self.params = Params.load(path)
        self.single_shot = single_shot



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
    '''
    def runner(self):
        self.action()
        if not self.single_shot:
            self.scheduler.enter(self.params.wait_time, 1, self.runner, ())
'''

    def run(self):
        collect = self.params.gc
        interval = self.params.wait_time
        max_iterations = self.params.scheduler_size
        if self.single_shot:
            self.action()
        else:
            #if collect:
            #    gc.set_debug(gc.DEBUG_LEAK)
            alive=True
            while alive:
                try:
                    print('*** starting new scheduler ***')
                    scheduler = SimpleScheduler(self.action, interval=interval, max_iterations=max_iterations)
                    alive=scheduler.run()
                    if collect:
                        print('Garbage collecting')
                        gc.collect(0)
                except KeyboardInterrupt:
                    alive=False
                except Exception as e:
                    print(f'Continuing after error : {e}')
            syslog(LogLevel.INFO, 'Exiting')



