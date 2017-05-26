import argparse
import sys
from . import func

def main(argv=sys.argv[1:]):
    if sys.version_info[0] != 3:
        raise OSError("only for python 3.5+")
    if sys.version_info[0] == 3 and sys.version_info[1] < 5:
        raise OSError("only for python 3.5+")
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    sub_parsers = subparsers.add_parser("sub")
    sub_group = sub_parsers.add_mutually_exclusive_group(required=False)
    sub_group.add_argument('-a', '--abc',type=str)
    sub_parsers.set_defaults(func=func)

    args = parser.parse_args()
    args.func(args)
