"""command for initializing python project."""
import argparse
from functools import partial
from pathlib import Path
import json
from pmfp.projectinfo import ProjectInfo


class InitPythonMixin:
    """initializing python project."""

    ENVS = ["env", "conda", "global"]

    def _init_python_universal_create_project(self, form, args):
        print("initializing python {} project!".format(form))
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="python",
            project_form=form
        )
        path = Path(".pmfprc.json")
        with open(str(path), 'w') as f:
            json.dump(obj.to_dict(), f)

        obj.init_project()
        if args.install:
            obj.install_requirements("requirement")
            if obj.form.env in ("env", "conda"):
                obj.install_requirements("dev")
        if args.with_docs:
            obj.init_docs()
        if args.with_dockerfile:
            obj.init_docker()
        if args.with_setup:
            obj.init_setup(
                manifesst=True,
                cython=args.cython,
                command=args.with_command,
                math=args.math
            )
        print("init python {} project done!".format(form))

    def _python_universal_parser(self, parser):
        parser.add_argument(
            '-e', '--env', type=str, choices=self.ENVS, default="env")
        parser.add_argument(
            '--with_setup', action='store_true', default=False)
        parser.add_argument(
            '--with_command', action='store_true', default=False)
        parser.add_argument(
            '--cython', action='store_true', default=False)
        parser.add_argument(
            '--math', action='store_true', default=False)
        parser.add_argument(
            '--with_dockerfile', action='store_true', default=False)
        parser.add_argument(
            '--with_docs', action='store_true', default=False)
        parser.add_argument(
            '--install', action='store_true', default=False)
        return parser

    def _python_default(self, parser):
        print("initializing python default project!")
        obj = ProjectInfo.input_info(
            template="simple",
            env='global',
            compiler="python",
            project_form='script'
        )
        path = Path(".pmfprc.json")
        with open(str(path), 'w') as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init python default project done!")

    def python(self):
        """Python argparse parsers."""
        parser = argparse.ArgumentParser(
            description='initialise a python project')
        parser.set_defaults(func=self._python_default)

        subparsers = parser.add_subparsers(
            dest='project_type', help="init a python project")

        # form is script
        script_parsers = subparsers.add_parser(
            "script", aliases=["S"], help="init a python script")
        script_parsers.add_argument(
            '-t',
            '--template',
            type=str,
            choices=[
                "sanic",
                "flask",
                "simple",
                "xmlrpc",
                "mprpc",
                'tk'
            ],
            default="simple"
        )
        script_parsers = self._python_universal_parser(script_parsers)

        _init_python_script = partial(self._init_python_universal_create_project, 'script')
        script_parsers.set_defaults(func=_init_python_script)

        # init python model
        model_parsers = subparsers.add_parser(
            "model", aliases=["M"], help="init a python model project")
        model_parsers.add_argument(
            '-t',
            '--template',
            type=str,
            choices=["simple", "keras", "command","pytorch"],
            default="simple"
        )
        model_parsers = self._python_universal_parser(model_parsers)
        _init_python_model = partial(self._init_python_universal_create_project, 'model')
        model_parsers.set_defaults(func=_init_python_model)

        # init python flask command
        flask_parsers = subparsers.add_parser(
            "flask",
            help="init a python gui project"
        )
        flask_parsers.add_argument(
            '-t',
            '--template',
            type=str,
            choices=[
                "admin",
                "api",
                "blueprint",
                "mvc"
            ],
            default="api"
        )
        flask_parsers = self._python_universal_parser(flask_parsers)
        _init_python_flask = partial(self._init_python_universal_create_project, 'flask')
        flask_parsers.set_defaults(func=_init_python_flask)

        # init python sanic command
        sanic_parsers = subparsers.add_parser(
            "sanic",
            help="init a python gui project"
        )
        sanic_parsers.add_argument(
            '-t',
            '--template',
            type=str,
            choices=[
                "api",
                "blueprint",
                "mvc",
                "socketio"
            ],
            default="api"
        )
        sanic_parsers = self._python_universal_parser(sanic_parsers)
        _init_python_sanic = partial(self._init_python_universal_create_project, 'sanic')
        sanic_parsers.set_defaults(func=_init_python_sanic)

        # init python celery command
        celery_parsers = subparsers.add_parser(
            "celery",
            aliases=["C"],
            help="init a python gui project"
        )
        celery_parsers.add_argument(
            '-t',
            '--template',
            type=str,
            choices=[
                "simple"
            ],
            default="simple"
        )
        celery_parsers = self._python_universal_parser(celery_parsers)
        _init_python_celery = partial(self._init_python_universal_create_project, 'celery')
        celery_parsers.set_defaults(func=_init_python_celery)

      
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def py(self):
        """Alias to python."""
        return self.python()


__all__ = ["InitPythonMixin"]
