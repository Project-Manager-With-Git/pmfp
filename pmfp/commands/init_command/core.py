import argparse


class InitCore:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='Project initialisation tool for Pythoner',
            usage='''ppm init <command> [<args>]

The most commonly used ppm init commands are:
   python/py        initialise a python project
   node             initialise a node project

''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        self.argv = argv
        args = parser.parse_args(argv[0:1])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()
