import gc

from .schedule import OneShotScheduler, Scheduler
from thermologger.common import Params, syslog, LogLevel



class RunLoop:

    def __init__(self,path,single_shot=False):
        self.params = Params.load(path)
        self.single_shot = single_shot

    def _collected(self,generation=0):
        try:
            return gc.get_stats()[generation]['collected']
        except:
            return None

    def run(self):
        collect = self.params.gc
        collected = self._collected(0)
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
                        print('Garbage collecting')
                        gc.collect(0)
                        new_collected=self._collected(0)
                        if new_collected is not None and collected is not None:
                            print(f'Garbage collected {new_collected-collected} objects')
                            collected=new_collected
                except KeyboardInterrupt:
                    alive=False
                except Exception as e:
                    print(f'Continuing after error : {e}')
            syslog(LogLevel.INFO, 'Exiting')



