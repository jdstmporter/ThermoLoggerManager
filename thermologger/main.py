#!/usr/bin/env python3
from .loop import RunLoop
from .common import CmdLineArgs,syslog
import gc

config_live='/etc/thermologger/config.json'
config_dev='config/config.json'


def run(args):

    try:
        parser = CmdLineArgs()
        if parser(args):
            #gc.enable()
            #gc.set_debug(gc.DEBUG_LEAK)
            #syslog.set_level(parser.log_level)
            loop = RunLoop(config_live if parser.is_live else config_dev,single_shot=parser.single_shot)
            loop.run()
        return 0
    except Exception as e:
        print(f'General error: {e}')










