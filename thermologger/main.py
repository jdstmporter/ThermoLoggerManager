#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentError
from .runloop import RunLoop





def run(args):
    parser = ArgumentParser(exit_on_error=False)
    parser.add_argument('-l',dest='mode',action='store_const',const='live',help='Live mode')
    parser.add_argument('-d', dest='mode', action='store_const', const='dev', help='Dev mode')
    try:
        opts = parser.parse_args(args)
        mode = opts.mode=='live'


        loop = RunLoop(is_live=mode)
        loop.run()


    except ArgumentError as e:
        print(f'Args are {args}')
        print(f'Error in provided options: {e}')
        parser.print_help()
    except Exception as e:
        print(f'General error: {e}')










