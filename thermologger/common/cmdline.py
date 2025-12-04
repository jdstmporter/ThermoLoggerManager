from argparse import ArgumentParser, ArgumentError
from .logs import LogLevel
from .hostinfo import HostInfo

class CmdLineArgs:


    def __init__(self):
        self.log_level = LogLevel.INFO
        self.is_live = False

    def __call__(self,args):
        parser = ArgumentParser(exit_on_error=False)
        ex = parser.add_mutually_exclusive_group()
        ex.add_argument('--live', '-l', dest='live', action='store_true', help='Live mode', required=False)
        ex.add_argument('--dev', '-d', dest='dev', action='store_true', help='Dev mode', required=False)

        log_names = [x.name for x in LogLevel]
        parser.add_argument('--loglevel', '-L',dest='loglevel',choices=log_names,type=str,default='INFO',required=False)
        try:
            opts = parser.parse_args(args)
            is_live = False
            if opts.live:
                is_live = True
                print('Specified live mode')
            elif opts.dev:
                is_live = False
                print('Specified dev mode')
            else:
                is_live = HostInfo.is_Server
                print(f'Computed mode: live={is_live}')

            self.is_live = is_live

            log_level = LogLevel.safe_named(opts.loglevel,LogLevel.INFO)
            print(f'Log level is {log_level.name}')
            self.log_level = log_level
            return True

        except ArgumentError as e:
            print(f'Args are {args}')
            print(f'Error in provided options: {e}')
            parser.print_help()
            return False

