import argparse
import json
from pathlib import Path
from libpmfp.projectinfo import ProjectInfo


class InitNodeMixin:

    def _init_node_script(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="node",
            project_type="script",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init node frontend project done!")
        return True

    def _init_node_frontend(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="node",
            project_type="frontend",
            with_test=args.without_test,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init node frontend project done!")
        return True

    def _init_node_vue(self, args):
        obj = ProjectInfo.input_info(
            template=args.template,
            env=args.env,
            compiler="node",
            project_type="vue",
            with_test=False,
            with_docs=args.without_docs,
            with_dockerfile=args.without_dockerfile)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init node vue project done!")
        return True

    def _init_node_default(self, args):
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
            '-e', '--env', type=str, choices=["node"], default="node")
        script_parsers.add_argument(
            '-t', '--template', type=str, choices=["es6", "ts"], default="es6")
        script_parsers.add_argument(
            '--without_test', action='store_false')
        script_parsers.add_argument(
            '--without_docs', action='store_false')
        script_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        script_parsers.set_defaults(func=self._init_node_script)

        # init node frontend command
        frontend_parsers = subparsers.add_parser(
            "frontend", aliases=["F"], help="init a node frontend project")
        frontend_parsers.add_argument(
            '-e', '--env', type=str, choices=["frontend"], default="frontend")
        frontend_parsers.add_argument(
            '-t', '--template', type=str, choices=["es6", "ts"], default="es6")
        frontend_parsers.add_argument(
            '--without_test', action='store_false')
        frontend_parsers.add_argument(
            '--without_docs', action='store_false')
        frontend_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        frontend_parsers.set_defaults(func=self._init_node_frontend)

        # init node vue command
        vue_parsers = subparsers.add_parser(
            "vue", aliases=["V"], help="init a node vue project")
        vue_parsers.add_argument(
            '-e', '--env', type=str, choices=["frontend"], default="frontend")
        vue_parsers.add_argument('-t', '--template', type=str,
                                 choices=["simple", "webpack", "webpack-simple"], default="webpack")
        vue_parsers.add_argument(
            '--without_docs', action='store_false')
        vue_parsers.add_argument(
            '--without_dockerfile', action='store_false')
        vue_parsers.set_defaults(func=self._init_node_vue)

        args = parser.parse_args(self.argv[1:])
        args.func(args)


__all__ = ["InitNodeMixin"]
