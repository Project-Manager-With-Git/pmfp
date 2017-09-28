import sys
import argparse
from pathlib import Path
from typing import Sequence
from libpmfp.projectinfo import ProjectInfo
from libpmfp.commands.status_command import status
from libpmfp.commands.init_command import Init
 
if sys.version_info[0] != 3:
    raise OSError("only for python 3.5+")
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    raise OSError("only for python 3.5+")


class PPM:

    def __init__(self,argv):
        parser = argparse.ArgumentParser(
            description='Project Manager for Pythoner',
            usage='''ppm <command> [<args>]

The most commonly used ppm commands are:
   init        initialise a project
   clean       clean a project
   status      see the project's info
   update      update the project's version
   upload      upload your project to a git repository, a docker repository,
               a pypi server
   test        test your project
   build       build your python project to a pyz file, wheel,egg,docker image,
               build your cpp project to a lib or a executable file
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

    def init(self):
        print('Running ppm init')
        if len(self.argv) == 1:
            path = Path(".pmfprc")
            if path.exists():
                if len([i for i in path.parent.iterdir() if not i.name.startswith(".")]) == 0:
                    obj = ProjectInfo.from_json(str(path))
                    obj.init_project()
                    return True
                else:
                    print("dir is not empty! if you want to rebuild the project run command clean first!")
                    return False
            else:
                print("please run this command in the root of the project, and initialise first")
                return False
        else:
            Init(self.argv[1:])
        print('Running ppm init done')

    def status(self):
        return status()

    # def update(self):
    #     parser = argparse.ArgumentParser(
    #         description='Download objects and refs from another repository')
    #     # NOT prefixing the argument with -- means it's not optional
    #     parser.add_argument('repository')
    #     args = parser.parse_args(self.argv[1:])
    #     print 'Running git fetch, repository=%s' % args.repository

    # def upload(self):
    #     parser = argparse.ArgumentParser(
    #         description='Download objects and refs from another repository')
    #     # NOT prefixing the argument with -- means it's not optional
    #     parser.add_argument('repository')
    #     args = parser.parse_args(self.argv[1:])
    #     print 'Running git fetch, repository=%s' % args.repository

    # def test(self):
    #     pass

    # def build(self):
    #     pass

    # def clean(self):
    #     pass


def main(argv: Sequence[str]=sys.argv[1:]):
    PPM(argv)