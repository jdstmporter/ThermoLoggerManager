from .schedule import OneShotScheduler, Scheduler
from thermologger.common import Params, syslog, LogLevel, GarbageCollect


class RunLoop:

    def __init__(self,path,single_shot=False):
        self.params = Params.load(path)
        self.single_shot = single_shot

    def run(self):
        collect = self.params.gc
        gc=GarbageCollect()
        interval = self.params.wait_time
        max_iterations = self.params.scheduler_size
        if self.single_shot:
            OneShotScheduler(self.params).run()
        else:
            #if collect:
            #    gc.set_debug(gc.DEBUG_LEAK)
            alive=True
            while alive:
                try:
                    print('*** starting new scheduler ***')
                    alive=Scheduler(self.params).run()
                    if collect:
                        gc()
                except KeyboardInterrupt:
                    alive=False
                except Exception as e:
                    print(f'Continuing after error : {e}')
            syslog(LogLevel.INFO, 'Exiting')



