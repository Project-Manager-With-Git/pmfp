"""ppm proto new命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_proto.cmd_proto_new import new_pb
from .core import ppm_proto


@ppm_proto.regist_subcmd
def new(argv: Sequence[str]) -> None:
    """使用默认模板创建新的protobuf文件.

    ppm proto new [-flag] <name>
    """
    parser = argparse.ArgumentParser(
        prog='ppm proto new',
        description='创建pb文件',
        usage=ppm_proto.subcmds.get("new").__doc__
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
