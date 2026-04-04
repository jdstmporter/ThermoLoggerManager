import gc
from thermologger.common import syslog,LogLevel

class GarbageCollect:
    def __init__(self):
        self.collected=self._collected(0)

    def _collected(self,generation=0) -> int|None:
        try:
            return gc.get_stats()[generation]['collected']
        except Exception as e:
            syslog(LogLevel.INFO,f'GC: {str(e)}')
            return None

    def __call__(self):
        print('Garbage collecting')
        gc.collect(0)
        new_collected = self._collected(0)
        if new_collected is not None and self.collected is not None:
            print(f'Garbage collected {new_collected - self.collected} objects')
            self.collected = new_collected
