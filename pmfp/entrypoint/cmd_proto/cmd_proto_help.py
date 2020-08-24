"""ppm proto help命令的处理."""
import argparse
from .core import ppm_proto
from typing import Sequence


@ppm_proto.regist_subcmd
def help(argv:Sequence[str]):
    """ppm proto help <subcommand>
ppm proto工具的子命令有:

    new                 创建一个protobuf文件
    build               编译protobuf到指定位置      
    """
    parser = argparse.ArgumentParser(
        prog='ppm proto help',
        description='查看子命令的帮助说明',
        usage= ppm_proto.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_proto.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)

def cmd_help(args:argparse.Namespace):
    print(ppm_proto.subcmds.get(args.subcmd).__doc__)