import sys
import argparse
from .command.echo import echo_command
from typing import Sequence


class Command:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='Project Manager for Pythoner',
            usage=''' <command> [<args>]
The most commonly used ppm commands are:
   echo        echo a string
''')
        parser.add_argument('command', help='Subcommand to run')

        self.argv = argv
        args = parser.parse_args(argv[0:1])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def echo(self):
        parser = argparse.ArgumentParser(
            description='echo string')
        parser.add_argument("command", type=str)
        parser.set_defaults(func=echo_command)
        args = parser.parse_args(self.argv[1:])
        args.func(args)


def main(argv: Sequence[str]=sys.argv[1:]):
    Command(argv)
