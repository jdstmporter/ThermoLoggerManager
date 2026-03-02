import multiprocessing
import sched
import time
from .action import Action


class Scheduler:

    def __init__(self,params):
        self.params=params
        self.interval = params.wait_time
        self.max_iterations = params.scheduler_size

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f'Exception: {exc_type}, {exc_val} {exc_tb}')
        self.end()
        return True


    def runner(self):
        act = Action(self.params)
        act()

    def runner_end(self):
        print('*** finalising')
        pass

    def run(self):
        try:
            iterations = 0
            while iterations < self.max_iterations:
                print(f'*** iteration {iterations}')
                self.runner()
                print(f'*** sleep for {self.interval}')
                time.sleep(self.interval)
                self.runner_end()
                iterations += 1
            return True
        except KeyboardInterrupt:
            return False

    def end(self):
        pass



class OneShotScheduler(Scheduler):

    def __init__(self,params):
        super().__init__(params)

    def run(self):
        self.runner()
        return True




















