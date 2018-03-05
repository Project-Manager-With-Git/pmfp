"""command for initializing python project."""
import argparse
from functools import partial
from pathlib import Path
import yaml
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
        path = Path(".pmfprc.yml")
        with open(str(path), 'w') as f:
            f.write(yaml.dump(obj.to_dict()))
        if args.install:
            obj.install_requirements("requirement")
            if obj.env in ("env", "conda"):
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
            '--with_doc', action='store_true', default=False)
        parser.add_argument(
            '--with_test', action='store_true', default=False)
        parser.add_argument(
            '--install', action='store_true', default=False)
        return parser

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
            choices=["simple"],
            default="simple"
        )
        model_parsers = self._python_universal_parser(model_parsers)
        _init_python_model = partial(self._init_python_universal_create_project, 'model')
        model_parsers.set_defaults(func=_init_python_model)

        # init python rpc command
        rpc_parsers = subparsers.add_parser(
            "rpc",
            aliases=["R"],
            help="init a python rpc project"
        )
        rpc_parsers.add_argument(
            '-t',
            '--template',
            type=str,
            choices=["xmlrpc", "mprpc"],
            default="xmlrpc"
        )
        rpc_parsers = self._python_universal_parser(rpc_parsers)
        _init_python_rpc = partial(self._init_python_universal_create_project, 'rpc')
        rpc_parsers.set_defaults(func=_init_python_rpc)

        # init python TK command
        gui_parsers = subparsers.add_parser(
            "gui",
            aliases=["G"],
            help="init a python gui project"
        )
        gui_parsers.add_argument(
            '-t',
            '--template',
            type=str,
            choices=["tk"],
            default="tk"
        )
        gui_parsers = self._python_universal_parser(gui_parsers)
        _init_python_gui = partial(self._init_python_universal_create_project, 'gui')
        gui_parsers.set_defaults(func=_init_python_gui)

    def py(self):
        """Alias to python."""
        return self.python()


__all__ = ["InitPythonMixin"]
