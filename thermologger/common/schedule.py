import sched
import time


class Scheduler:

    def __init__(self,task,interval : int = 60, max_iterations = None):
        self.task = task
        self.interval = interval
        self.infinite = max_iterations is None
        self.max_iterations = max_iterations
        self.iterations = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f'Exception: {exc_type}, {exc_val} {exc_tb}')
        self.end()
        return True

    def should_run(self):
        return self.infinite or self.iterations < self.max_iterations

    def action(self):
        if self.should_run():
            self.task()
            self.iterations+=1

    def run(self):
        self.iterations = 0
        return True

    def end(self):
        pass

class SchedScheduler(Scheduler):

    def __init__(self,task,interval : int = 60, max_iterations = None):
        super().__init__(task,interval,max_iterations)
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def _runner(self):
        print(f'*** iteration {self.iterations}')
        self.action()
        if self.should_run():
            self.scheduler.enter(self.interval, 1, self._runner, ())

    def run(self):
        super().run()
        self.scheduler.enter(self.interval, 1, self._runner, ())
        try:
            self.scheduler.run()
            return True
        except KeyboardInterrupt:
            return False



class SimpleScheduler(Scheduler):

    def __init__(self,task,interval : int = 60, max_iterations = None):
        super().__init__(task, interval, max_iterations)

    def run(self):
        super().run()
        try:
            while self.should_run():
                print(f'*** iteration {self.iterations}')
                time.sleep(self.interval)
                self.action()
            return True
        except KeyboardInterrupt:
            return False












