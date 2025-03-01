import time
import sys
import enum


class LogLevel(enum.IntEnum):
    DEBUG = 0
    INFO = 1
    ERROR = 2

    @classmethod
    def named(cls,name : str):
        name=name.upper()
        return cls.__members__[name]


def logLambda(obj,level):
    def action(message):
        return obj(level,message)
    return action


class Log:

    def __init__(self, logfile='syslog.log', loglevel = LogLevel.DEBUG):
        self.file = open(logfile, 'a')
        self.loglevel = loglevel

    def __del__(self):
        # noinspection PyBroadException
        try:
            self.file.close()
        except:
            pass

    def __call__(self, loglevel : LogLevel, message : str):
        if loglevel >= self.loglevel:
            self.file.write(f'{loglevel} {time.time()} : {message}\n')
            sys.stderr.write(f'{loglevel} {time.time()} : {message}\n')

    def __getattr__(self,name : str):
        try:
            level=LogLevel.named(name)
            return logLambda(self,level)
        except KeyError as e:
            self(LogLevel.ERROR,f'Unknown log level {name}')
            self.exc(e)
        except Exception as e:
            print(str(e))
            self.exc(e)

    def exc(self, e):
        self(LogLevel.ERROR, str(e))
        self(LogLevel.ERROR, repr(e))




syslog = Log()

if __name__ == '__main__':
    print(LogLevel.__members__)
    syslog.error('fred')
