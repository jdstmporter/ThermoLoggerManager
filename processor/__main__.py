import argparse
from .main import run

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d','--days', type=int)
group.add_argument('-n', '--count', type=int)
args = parser.parse_args()

run(args)
