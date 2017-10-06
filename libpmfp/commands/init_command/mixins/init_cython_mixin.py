import argparse
import json
from pathlib import Path
from libpmfp.projectinfo import ProjectInfo


class InitCythonMixin:

    def _init_cython_command(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="cython",
            project_type="command",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init cython command-line application done!")
        return True

    def _init_cython_model(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="cython",
            project_type="model",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init cython model done!")
        return True

    def _init_cython_script(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="cython",
            project_type="script",
            with_test=False,
            with_docs=False,
            with_dockerfile=False)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init cython script done!")
        return True

    def _init_cython_celery(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="cython",
            project_type="celery",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init cython celery project done!")
        return True

    def cython(self):
        parser = argparse.ArgumentParser(
            description='initialise a cython project')
        parser.set_defaults(func=lambda args: print("default"))

        subparsers = parser.add_subparsers(
            dest='project_type', help="init a cython project")

        # init python command-line command
        command_parsers = subparsers.add_parser(
            "command-line", aliases=["command", "C"], help="init a cython command-line project")
        command_parsers.add_argument(
            '-e', '--env', type=str, choices=["env", "conda"], default="env")
        command_parsers.add_argument('-t', '--template', type=str, choices=[
            "simple", "math"],
            default="simple")
        command_parsers.add_argument(
            '--without_test', action='store_false')
        command_parsers.add_argument(
            '--without_docs', action='store_false')
        command_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        command_parsers.add_argument(
            '--install', action='store_true')
        command_parsers.set_defaults(func=self._init_cython_command)

        # init python model command
        model_parsers = subparsers.add_parser(
            "model", aliases=["M"], help="init a cython model project")
        model_parsers.add_argument(
            '-e', '--env', type=str, choices=["env", "conda"], default="env")
        model_parsers.add_argument('-t', '--template', type=str, choices=[
            "simple", "math"],
            default="simple")
        model_parsers.add_argument(
            '--without_test', action='store_false')
        model_parsers.add_argument(
            '--without_docs', action='store_false')
        model_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        model_parsers.add_argument(
            '--install', action='store_true')
        model_parsers.set_defaults(func=self._init_cython_model)

        # init python script command
        script_parsers = subparsers.add_parser(
            "script", aliases=["S"], help="init a cython script")
        script_parsers.add_argument(
            '-e', '--env', type=str, choices=["env", "conda"], default="env")
        script_parsers.add_argument('-t', '--template', type=str, choices=[
            "simple", "math"],
            default="simple")

        script_parsers.add_argument(
            '--install', action='store_true')
        script_parsers.set_defaults(func=self._init_cython_script)

        # init python celery command
        celery_parsers = subparsers.add_parser(
            "celery", aliases=["C"], help="init a celery project for cython")
        celery_parsers.add_argument(
            '-e', '--env', type=str, choices=["env", "conda"], default="env")
        celery_parsers.add_argument('-t', '--template', type=str, choices=[
            "simple", "math"],
            default="simple")
        celery_parsers.add_argument(
            '--without_test', action='store_false')
        celery_parsers.add_argument(
            '--without_docs', action='store_false')
        celery_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        celery_parsers.add_argument(
            '--install', action='store_true')
        celery_parsers.set_defaults(func=self._init_cython_celery)

        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def cy(self):
        return self.cython()


__all__ = ["InitCythonMixin"]
