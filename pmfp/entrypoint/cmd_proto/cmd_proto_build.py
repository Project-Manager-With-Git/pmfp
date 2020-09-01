"""ppm proto build命令的处理."""
import argparse
from .core import ppm_proto
from typing import Sequence
from pmfp.features.cmd_proto.cmd_proto_build import build_pb


@ppm_proto.regist_subcmd
def build(argv:Sequence[str])->None:
    """ppm proto build [-flag] <files>

    编译proto文件
    """
    parser = argparse.ArgumentParser(
        prog='ppm proto build',
        description='编译pb文件',
        usage= ppm_proto.subcmds.get("build").__doc__
    )
    parser.add_argument("-e", "--env", nargs='+',type=str,choices=("py","js","go","web"), required=True,help="编译为什么语言或环境")
    parser.add_argument("-I", "--includes", nargs='+', type=str,required=True, help="待编译的文件的依赖所在的文件夹")
    parser.add_argument("-g","--grpc", action="store_true", help="是否是grpc")
    parser.add_argument("-t", "--to", type=str,required=True, help="存放的地方")
    parser.add_argument("-s","--source_relative", action="store_true", help="使用路径作为包名,只针对go语言")
    parser.add_argument("-k","--kwargs",type=str, help="其他键值对的额外参数,使用`key::value,key::value`的形式")
    parser.add_argument("files",nargs='+', type=str, help="待编译的文件名")
    parser.set_defaults(func=cmd_build_pb)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_build_pb(args: argparse.Namespace)->None:
    if not args.includes:
        args.includes = []
    build_pb(env=args.env,files=args.files,includes=args.includes,to=args.to,grpc=args.grpc,source_relative=args.source_relative)
