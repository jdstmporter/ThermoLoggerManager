from .meteorologyAction import MeteorologyAction

from thermologger.common import Params, syslog, LogLevel, GarbageCollect

class MeteorologyRunLoop:

    def __init__(self,path,single_shot=False):
        self.params = Params.load(path)
        self.single_shot = single_shot
        print(str(self.params))


    def runner(self):
        proc=MeteorologyAction(self.params)
        proc()



    def run(self):
        if self.single_shot:
            self.runner()
        else:
            alive = True
            interval = self.params.meteo.interval
            gc = GarbageCollect()
            while alive:
                try:
                    self.runner()
                    time.sleep(interval)
                    if collect:
                        gc()
                except KeyboardInterrupt:
                    alive = False
                except Exception as e:
                    print(f'Continuing after error : {e}')
            syslog(LogLevel.INFO, 'Exiting')





