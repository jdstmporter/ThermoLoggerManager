import time
import sys
import enum
import traceback


class LogLevel(enum.IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    @classmethod
    def named(cls,name : str):
        name=name.upper()
        return cls.__members__[name]


def logLambda(obj,level):
    def action(message):
        return obj(level,message)
    return action


class Log:

    def __init__(self, logfile='syslog.log', loglevel = LogLevel.DEBUG, encoding='utf-8'):
        self.file = open(logfile, 'ab')
        self.loglevel = loglevel
        self.encoding = encoding

    def __del__(self):
        # noinspection PyBroadException
        try:
            self.file.close()
        except:
            pass

    def __call__(self, loglevel : LogLevel, message : str):
        if loglevel >= self.loglevel:
            msg = Log.LogLine(loglevel,message)+'\n'
            self.file.write(msg.encode(self.encoding))
            sys.stderr.write(msg)

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

    @classmethod
    def LogLine(cls,loglevel,message):
        return f'{loglevel} {time.time()} : {message}'

    def exc(self, e):
        self(LogLevel.ERROR, str(e))
        self(LogLevel.ERROR, repr(e))

    def _parse_exc_info(self,args):
        if len(args) == 1: return args[0]
        elif len(args) == 3: return args[1]
        else: return sys.exception()

    def exception(self, *args):
        exc = self._parse_exc_info(args)
        lines = traceback.format_exception(exc)
        self(LogLevel.CRITICAL,f"Exception {exc}")
        for line in range(len(lines)):
            self(LogLevel.CRITICAL,f"{line}    : {lines[line]}")

    @property
    def isDebug(self):
        return self.loglevel==LogLevel.DEBUG



syslog = Log()

if __name__ == '__main__':
    print(LogLevel.__members__)
    syslog.error('fred')
