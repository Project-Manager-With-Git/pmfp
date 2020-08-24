"""ppm proto new命令的处理."""
import argparse
from .core import ppm_proto
from typing import Sequence
from pmfp.features.cmd_proto.cmd_proto_new import new_pb


@ppm_proto.regist_subcmd
def new(argv:Sequence[str]):
    """ppm proto new

    创建新的protobuf文件
    """
    parser = argparse.ArgumentParser(
        prog='ppm proto new',
        description='创建pb文件',
        usage= ppm_proto.subcmds.get("build").__doc__
    )
    parser.add_argument("-g","--grpc", action="store_true", help="是否是grpc")
    parser.add_argument("-t", "--to", type=str,required=True, help="存放的地方")
    parser.add_argument("-p", "--parent_package", type=str, help="package父package")
    parser.add_argument("name",type=str, help="proto文件名,也是package名")
    parser.set_defaults(func=cmd_new_pb)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_new_pb(args: argparse.Namespace):
    new_pb(name=args.name,to=args.to,grpc=args.grpc,parent_package=args.parent_package)
