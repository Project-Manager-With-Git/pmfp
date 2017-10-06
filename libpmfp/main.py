import sys
import argparse
from pathlib import Path
from typing import Sequence
from libpmfp.projectinfo import ProjectInfo
from libpmfp.commands.status_command import status
from libpmfp.commands.init_command import Init
from libpmfp.commands.clean_command import clean
from libpmfp.commands.install_command import install
from libpmfp.commands.update_command import update
from libpmfp.commands.upload_command import upload
#from libpmfp.commands.run_command import run

if sys.version_info[0] != 3:
    raise OSError("only for python 3.5+")
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    raise OSError("only for python 3.5+")


class PPM:

    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='Project Manager for Pythoner',
            usage='''ppm <command> [<args>]

The most commonly used ppm commands are:
   init        initialise a project
   clean       clean a project
   install     install a package
   status      see the project's info
   update      update the project's version and status
   upload      upload your project to a git repository, a docker repository,
               a pypi server
   
   run         run scripts for python and node
   build       build your python project to a pyz file, wheel,egg,docker image,
               build your cpp project to a lib or a executable file
   test        test your project
   doc         build your project's document
   
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
                    print(
                        "dir is not empty! if you want to rebuild the project run command clean first!")
                    return False
            else:
                print(
                    "please run this command in the root of the project, and initialise first")
                return False
        else:
            Init(self.argv[1:])
        print('Running ppm init done')

    def status(self):
        return status()

    def clean(self):
        parser = argparse.ArgumentParser(
            description='clean a project')
        parser.add_argument(
            '-A', '--all', action='store_true')
        parser.set_defaults(func=clean)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def install(self):
        parser = argparse.ArgumentParser(
            description='install a package for this project')
        parser.add_argument('packages', nargs='?', type=str, default="DEFAULT")
        parser.add_argument(
            '-D', '--dev', action='store_true')
        parser.add_argument(
            '-T', '--test', action='store_true')
        parser.add_argument(
            '-A', '--all', action='store_true')
        parser.set_defaults(func=install)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("install done!")

    def update(self):
        parser = argparse.ArgumentParser(
            description="update this project's version and status")
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('version', type=str)
        parser.add_argument('-S', "--status", type=str,
                            choices=["dev", "testing", "release", "stable"], default="dev")
        parser.set_defaults(func=update)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("update done!")

    def upload(self):
        parser = argparse.ArgumentParser(
            description='upload project to a remote repository')
        parser.add_argument('-g', '--git', type=str,
                                  nargs='*', required=False)
        parser.set_defaults(func=upload)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("upload done!")


    def run(self):
        parser = argparse.ArgumentParser(
            description='upload project to a remote repository')
        parser.add_argument('script', type=str,
                                  nargs='*', required=False)
        parser.set_defaults(func=run)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("run script done!")

    def build(self):
        pass


    def test(self):
        parser = argparse.ArgumentParser(
            description='upload project to a remote repository')
        parser.add_argument('-g', '--git', type=str,
                                  nargs='*', required=False)
        parser.set_defaults(func=upload)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("upload done!")

    def doc(self):
        parser = argparse.ArgumentParser(
            description='upload project to a remote repository')
        parser.add_argument('-g', '--git', type=str,
                                  nargs='*', required=False)
        parser.set_defaults(func=upload)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("upload done!")


    


def main(argv: Sequence[str]=sys.argv[1:]):
    PPM(argv)
