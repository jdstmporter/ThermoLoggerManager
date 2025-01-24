import time


class Log:
    DEBUG = "Debug"
    INFO = "Info"
    ERROR = "Error"

    def __init__(self, logfile='syslog.log'):
        self.file = open(logfile, 'a')

    def __del__(self):
        # noinspection PyBroadException
        try:
            self.file.close()
        except:
            pass

    def __call__(self, loglevel, message):
        self.file.write(f'{loglevel} {time.time()} : {message}\n')
        # sys.stderr.write(f'{loglevel} {time.time()} : {message}\n')

    def exc(self, e):
        self(Log.ERROR, str(e))
        self(Log.ERROR, repr(e))


syslog = Log()