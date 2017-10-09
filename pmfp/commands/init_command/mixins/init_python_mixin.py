import argparse
import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


class InitPythonMixin:

    def _init_python_web(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="python",
            project_type="web",
            with_test=False,
            with_docs=False,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init python web application done!")
        return True

    def _init_python_gui(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="python",
            project_type="gui",
            with_test=False,
            with_docs=False,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init python gui application done!")
        return True

    def _init_python_command(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="python",
            project_type="command",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init python command-line application done!")
        return True

    def _init_python_model(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="python",
            project_type="model",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init python model done!")
        return True

    def _init_python_script(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="python",
            project_type="script",
            with_test=False,
            with_docs=False,
            with_dockerfile=False)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init python script done!")
        return True

    def _init_python_celery(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="python",
            project_type="celery",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(args.install)
        print("init python celery project done!")
        return True

    def _python_default(self, args):
        obj = ProjectInfo.input_info(
            template="simple",
            env="env",
            compiler="python",
            project_type="script",
            with_test=False,
            with_docs=False,
            with_dockerfile=False)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(install=True)
        print("init python default script done!")
        return True

    def python(self):
        parser = argparse.ArgumentParser(
            description='initialise a python project')
        parser.set_defaults(func=self._python_default)

        subparsers = parser.add_subparsers(
            dest='project_type', help="init a python project")
        web_parsers = subparsers.add_parser(
            "web", aliases=["W"], help="init a python web project")
        web_parsers.add_argument(
            '-e', '--env', type=str, choices=["env", "conda"], default="env")
        web_parsers.add_argument('-t', '--template', type=str, choices=[
            "sanic", "flask",
            "sanic_socketio", "flask_socketio"
            "sanic_api", "flask_api",
            "sanic_mvc", "flask_mvc",
            "sanic_blueprints",
            "flask_blueprints"],
            default="flask")
        web_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        web_parsers.add_argument(
            '--install', action='store_true')
        web_parsers.set_defaults(func=self._init_python_web)

        # init python gui command
        gui_parsers = subparsers.add_parser(
            "gui", aliases=["G"], help="init a python gui project")
        gui_parsers.add_argument(
            '-e', '--env', type=str, choices=["env", "conda"], default="env")
        gui_parsers.add_argument('-t', '--template', type=str, choices=[
            "tk", "tk_mvc"],
            default="tk")

        gui_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        gui_parsers.add_argument(
            '--install', action='store_true')
        gui_parsers.set_defaults(func=self._init_python_gui)

        # init python command-line command
        command_parsers = subparsers.add_parser(
            "command-line", aliases=["command", "C"], help="init a python command-line project")
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
        command_parsers.set_defaults(func=self._init_python_command)

        # init python model command
        model_parsers = subparsers.add_parser(
            "model", aliases=["M"], help="init a python model project")
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
        model_parsers.set_defaults(func=self._init_python_model)

        # init python script command
        script_parsers = subparsers.add_parser(
            "script", aliases=["S"], help="init a python script")
        script_parsers.add_argument(
            '-e', '--env', type=str, choices=["env", "conda"], default="env")
        script_parsers.add_argument('-t', '--template', type=str, choices=[
            "simple", "math"],
            default="simple")
        script_parsers.add_argument(
            '--install', action='store_true')
        script_parsers.set_defaults(func=self._init_python_script)

        # init python celery command
        celery_parsers = subparsers.add_parser(
            "celery", aliases=["C"], help="init a celery project")
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
        celery_parsers.set_defaults(func=self._init_python_celery)

        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def py(self):
        return self.python()


__all__ = ["InitPythonMixin"]
