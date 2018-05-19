"""命令行命令定义."""
import sys
import argparse
from pathlib import Path
from typing import Sequence
from pmfp.projectinfo import ProjectInfo
from pmfp.commands.status_command import status
from pmfp.commands.init_command import Init
from pmfp.commands.clean_command import clean
from pmfp.commands.install_command import install
from pmfp.commands.update_command import update
from pmfp.commands.upload_command import upload
from pmfp.commands.run_command import run
from pmfp.commands.build_command import build
from pmfp.commands.test_command import test
from pmfp.commands.doc_command import doc
from pmfp.commands.new_command import new
from pmfp.commands.flask_command import flask
from pmfp.commands.sanic_command import sanic
from pmfp.commands.celery_command import celery
from pmfp.commands.vue_command import vue

if sys.version_info[0] != 3:
    raise OSError("only for python 3.5+")
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    raise OSError("only for python 3.5+")


class PPM:
    """ppm命令的第一级子命令定义."""

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
               
   test        test your project
   doc         build your project's document
   new         new a document,setup.py,test,dockerfile

shortcut:
   flask       init flask
   sanic       init sanic
   vue         init vue
   celery      init celery
   
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
        """创建对应模板项目的子命令"""
        print('Running ppm init')
        if len(self.argv) == 1:
            path = Path(".pmfprc.json")
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
        """查看项目状态的命令."""
        return status()

    def clean(self):
        """清理项目,删除文件."""
        parser = argparse.ArgumentParser(
            description='clean a project')
        parser.add_argument(
            '-A', '--all', action='store_true')
        parser.set_defaults(func=clean)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def install(self):
        """为项目安装依赖.如果有参数就是安装到固定环境,没有就是按固定环境安装其中写的内容."""
        parser = argparse.ArgumentParser(
            description='install a package for this project')
        parser.add_argument('packages', nargs='?', type=str, default="DEFAULT")
        parser.add_argument(
            '-D', '--dev', action='store_true')
        parser.add_argument(
            '-A', '--all', action='store_true')
        parser.set_defaults(func=install)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("install done!")

    def update(self):
        """更新项目元数据."""
        parser = argparse.ArgumentParser(
            description="update this project's version and status")
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('-V', '--version', type=str)
        parser.add_argument('-S', "--status", type=str,
                            choices=["dev", "testing", "release", "production"])
        parser.set_defaults(func=update)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("update done!")

    def upload(self):
        """上传数据."""
        parser = argparse.ArgumentParser(
            description='upload project to a remote repository')
        parser.add_argument('-g', '--git', type=str,
                                  nargs='*', required=False)
        parser.add_argument('-t', '--git_tag', action="store_true", default=False)
        parser.set_defaults(func=upload)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("upload done!")

    def run(self):
        """执行命令的命令."""
        parser = argparse.ArgumentParser(
            description='run a script')
        parser.add_argument('script', type=str,
                            nargs='*')
        parser.set_defaults(func=run)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("run script done!")

    def build(self):
        """按需求编译项目为二进制文件.

        包括编译dockerfile
        python可以选择将包编译为egg或者wheel用于发布,或者编译为pyz文件用于部署.
        node和c暂时不支持.
        """
        parser = argparse.ArgumentParser(
            description='build project to a remote repository')

        parser.add_argument(
            '-e', '--egg', action="store_true", default=False)
        parser.add_argument(
            '-w', '--wheel', action="store_true", default=False)
        parser.add_argument(
            '-c', '--cython', action="store_true", default=False)
        parser.add_argument(
            '-z', '--pyz', action="store_true", default=False)
        parser.add_argument(
            '-a', '--app', action="store_true", default=False)
        parser.add_argument(
            '-d', '--docker', action="store_true", default=False)

        parser.set_defaults(func=build)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("build package done!")

    def test(self):
        """测试命令的参数设置."""
        parser = argparse.ArgumentParser(
            description='test project')
        parser.add_argument('-H', '--html', action="store_true", default=False,
                            help="export the html report")
        parser.add_argument('-g', action="store_true", default=False,
                            help="use global env")
        parser.add_argument(
            '-T', '--typecheck', action="store_true", help="check python's typehints")
        parser.add_argument('-S', '--stress', action="store_true",
                            help="stress test for web server")
        parser.set_defaults(func=test)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("test done!")

    def doc(self):
        """用于构建文档"""
        parser = argparse.ArgumentParser(
            description="build project's document")
        parser.add_argument('-s', '--serve', action="store_true")
        parser.set_defaults(func=doc)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("doc done!")

    def new(self):
        """创建一些单独的模块."""
        parser = argparse.ArgumentParser(
            description='new a document,setup.py,test,dockerfile for a project')
        parser.add_argument("command", type=str, choices=[
                            'document', 'setup.py', 'dockerfile', 'main', 'cython'])
        parser.add_argument("-n", "--name", type=str, help="指定cython模块的名字", default="cymodel")
        parser.add_argument("-t", "--to", type=str, help="setup.py指定一个存放的位置", default=".")
        parser.add_argument("-y", "--with_cython", action="store_true", help="setup.py指定是否要使用cython", default=False)
        parser.add_argument("-c", "--command", action="store_true", help="setup.py指定是否要设置endpoint", default=False)
        parser.add_argument("-m", "--math", action="store_true", help="为cython的setup.py指定是否引入numpy的头文件", default=False)

        parser.set_defaults(func=new)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("new done!")

    def flask(self):
        """快速构建sanic项目."""
        parser = argparse.ArgumentParser(
            description='initialise a flask project')
        parser.add_argument(
            '-e', '--env', type=str, choices=["env", "conda", "global"], default="env")
        parser.add_argument('-t', '--template', type=str, choices=[
            'admin',
            "api",
            "mvc",
            "blueprints"],
            default="api")
        parser.set_defaults(func=flask)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("flask init done!")

    def sanic(self):
        """快速构造sanic项目."""
        parser = argparse.ArgumentParser(
            description='initialise a sanic project')
        parser.add_argument(
            '-e', '--env', type=str, choices=["env", "conda", "global"], default="env")
        parser.add_argument('-t', '--template', type=str, choices=[
            "socketio",
            "api",
            "mvc",
            "blueprints"],
            default="api")
        parser.set_defaults(func=sanic)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("sanic init done!")

    def celery(self):
        """快速构造celery项目."""
        parser = argparse.ArgumentParser(
            description='initialise a celery project')
        parser.add_argument(
            '-e', '--env', type=str, choices=["env", "conda", "global"], default="env")
        parser.set_defaults(func=celery)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("celery init done!")

    def vue(self):
        pass


def main(argv: Sequence[str]=sys.argv[1:]):
    PPM(argv)
