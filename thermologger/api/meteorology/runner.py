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
            self._action()
        else:
            alive = True
            gc = GarbageCollect()
            max_iterations = self.params.scheduler_size
            while alive:
                try:
                    iterations=0
                    while iterations<self.max_iterations:
                        self.runner()
                        time.sleep(3600)
                        iterations+=1
                    print('*** starting new meteoscheduler ***')
                    if collect:
                        gc()
                except KeyboardInterrupt:
                    alive = False
                except Exception as e:
                    print(f'Continuing after error : {e}')
            syslog(LogLevel.INFO, 'Exiting')





def run(path):
    try:
        m=MeteorologyRunLoop(path,True)
        m.run()
    except Exception as e:
        print(str(e))