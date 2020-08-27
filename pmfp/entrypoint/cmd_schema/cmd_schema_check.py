"""ppm schema check命令的处理."""
import argparse
from .core import ppm_proto
from typing import Sequence
from pmfp.features.cmd_proto.cmd_proto_build import build_pb


@ppm_proto.regist_subcmd
def build(argv:Sequence[str]):
    """ppm proto build

    编译proto文件
    """
    parser = argparse.ArgumentParser(
        prog='ppm proto build',
        description='编译pb文件',
        usage= ppm_proto.subcmds.get("build").__doc__
    )
    parser.add_argument("-s", "--schema",type=str, required=True,help="指定需要满足的jsonschema格式文件")
    
    parser.add_argument("files",nargs='+', type=str, help="待编译的文件名")
    parser.set_defaults(func=cmd_build_pb)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_build_pb(args: argparse.Namespace):
    if not args.includes:
        args.includes = []
    build_pb(env=args.env,files=args.files,includes=args.includes,to=args.to,grpc=args.grpc,source_relative=args.source_relative)
