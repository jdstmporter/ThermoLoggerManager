#!/usr/bin/env python3


from .runloop import RunLoop
from .common import CmdLineArgs,syslog

config_live='/etc/thermologger/config.json'
config_dev='config/config.json'


def run(args):

    try:
        parser = CmdLineArgs()
        if parser(args):
            syslog.set_level(parser.log_level)
            loop = RunLoop(config_live if parser.is_live else config_dev)
            loop.run()
        return 0


    except Exception as e:
        print(f'General error: {e}')










