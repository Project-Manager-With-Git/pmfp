import argparse
import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


class InitCppMixin:
    """初始化C/Cpp项目的混入;"""
    def _init_cpp_command(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="cpp",
            project_type="command",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init cpp command-line application done!")
        return True

    def _init_cpp_model(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="cpp",
            project_type="model",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init cpp model done!")
        return True

    def _cpp_default(self,args):
        obj = ProjectInfo.input_info(
            template="source",
            env="g++",
            compiler="cpp",
            project_type="model",
            with_test=False,
            with_docs=False,
            with_dockerfile=False)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init cpp default done!")
        return True


    def cpp(self):
        parser = argparse.ArgumentParser(
            description='initialise a cpp project')
        parser.set_defaults(func=self._cpp_default)

        subparsers = parser.add_subparsers(
            dest='project_type', help="init a cpp project")

        # init python command-line command
        command_parsers = subparsers.add_parser(
            "command-line", aliases=["command", "C"], help="init a cpp command-line project")
        command_parsers.add_argument(
            '-e', '--env', type=str, choices=["g++", "clang"], default="g++")
        command_parsers.add_argument('-t', '--template', type=str, choices=[
            "source"],
            default="source")
        command_parsers.add_argument(
            '--without_test', action='store_false')
        command_parsers.add_argument(
            '--without_docs', action='store_false')
        command_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        command_parsers.set_defaults(func=self._init_cpp_command)

        # init python model command
        model_parsers = subparsers.add_parser(
            "model", aliases=["M"], help="init a cpp model project")
        model_parsers.add_argument(
            '-e', '--env', type=str, choices=["gcc", "clang"], default="gcc")
        model_parsers.add_argument('-t', '--template', type=str, choices=[
            "source","header"],
            default="source")
        model_parsers.add_argument(
            '--without_test', action='store_false')
        model_parsers.add_argument(
            '--without_docs', action='store_false')
        model_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        model_parsers.set_defaults(func=self._init_cpp_model)

        args = parser.parse_args(self.argv[1:])
        args.func(args)


__all__ = ["InitCppMixin"]