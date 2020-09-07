"""ppm proto new命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_project.cmd_project_init import init_project
from .core import ppm_project


@ppm_project.regist_subcmd
def init(argv: Sequence[str]) -> None:
    """创建一个新项目.

    ppm proto init [-flag]
    """
    parser = argparse.ArgumentParser(
        prog='ppm proto new',
        description='创建pb文件',
        usage=ppm_project.subcmds.get("new").__doc__
    )
    parser.add_argument("-g", "--grpc", action="store_true",
                        help="是否是grpc")
    parser.add_argument("-t", "--to", type=str,
                        default=".", help="存放的地方")
    parser.add_argument("-p", "--parent_package", type=str,
                        help="package父package")
    parser.add_argument("name", type=str,
                        help="proto文件名,也是package名")
    parser.set_defaults(func=cmd_new_pb)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_new_pb(args: argparse.Namespace) -> None:
    """新建一个protobuf."""
    new_pb(name=args.name, to=args.to, grpc=args.grpc, parent_package=args.parent_package)
