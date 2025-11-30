#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentError
from .runloop import RunLoop
from .common import HostInfo

config_live='/etc/thermologger/config.json'
config_dev='config/config.json'


def run(args):
    parser = ArgumentParser(exit_on_error=False)
    ex = parser.add_mutually_exclusive_group()
    ex.add_argument('--live','-l',dest='live',action='store_true',help='Live mode',required=False)
    ex.add_argument('--dev','-d', dest='dev',action='store_true', help='Dev mode',required=False)
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

        loop = RunLoop(config_live if is_live else config_dev)
        loop.run()


    except ArgumentError as e:
        print(f'Args are {args}')
        print(f'Error in provided options: {e}')
        parser.print_help()
    except Exception as e:
        print(f'General error: {e}')










