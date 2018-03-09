"""command for initializing node project."""
import argparse
import json
from pathlib import Path
from functools import partial
from pmfp.projectinfo import ProjectInfo


class InitNodeMixin:
    """初始化Node项目的混入."""
    def _init_node_universal_create_project(self, form, args):
        print("initializing Node {} project!".format(form))
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="node",
            project_form=form
        )
        path = Path(".pmfprc.json")
        with open(str(path), 'w') as f:
            json.dump(obj.to_dict(), f)

        obj.init_project()
        if args.with_docs:
            obj.init_docs()
        if args.with_dockerfile:
            obj.init_docker()
        print("init Node {} project done!".format(form))

    def _init_node_default(self, args):
        print("initializing Node default project!")
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="node",
            project_form=form
        )
        path = Path(".pmfprc.json")
        with open(str(path), 'w') as f:
            json.dump(obj.to_dict(), f)

        obj.init_project()
        print("init Node default project done!")

        obj = ProjectInfo.input_info(
            template="es6",
            env="es6",
            compiler="node",
            project_type="frontend",
            with_test=False,
            with_docs=False,
            with_dockerfile=False)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init node frontend project done!")
        return True

    def _node_universal_parser(self, parser):
        parser.add_argument(
            '-e', '--env', type=str, choices=["node"], default="node")
        parser.add_argument(
            '--with_dockerfile', action='store_true', default=False)
        parser.add_argument(
            '--with_docs', action='store_true', default=False)
        return parser

    def node(self):
        parser = argparse.ArgumentParser(
            description='initialise a node project')
        parser.set_defaults(func=self._init_node_default)

        subparsers = parser.add_subparsers(
            dest='project_type', help="init a node project")

        # init node script
        script_parsers = subparsers.add_parser(
            "script", aliases=["S"], help="init a node script")

        script_parsers.add_argument(
            '-t', '--template', type=str, choices=["es6", "ts"], default="es6")
        script_parsers = self._node_universal_parser(script_parsers)
        _init_node_script = partial(self._init_node_universal_create_project, 'script')
        script_parsers.set_defaults(func=_init_node_script)

        # init node frontend command
        frontend_parsers = subparsers.add_parser(
            "frontend", aliases=["F"], help="init a node frontend project")

        frontend_parsers.add_argument(
            '-t', '--template', type=str, choices=["es6", "ts"], default="es6")
        frontend_parsers = self._node_universal_parser(frontend_parsers)
        _init_node_frontend = partial(self._init_node_universal_create_project, 'frontend')
        frontend_parsers.set_defaults(func=_init_node_frontend)

        # init node vue command
        vue_parsers = subparsers.add_parser(
            "vue", aliases=["V"], help="init a node vue project")

        vue_parsers.add_argument('-t', '--template', type=str,
                                 choices=["webpack"], default="webpack")
        vue_parsers = self._node_universal_parser(vue_parsers)
        _init_node_vue = partial(self._init_node_universal_create_project, 'vue')
        vue_parsers.set_defaults(func=_init_node_vue)

        args = parser.parse_args(self.argv[1:])
        args.func(args)


__all__ = ["InitNodeMixin"]
