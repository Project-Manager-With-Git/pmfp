"""help命令的处理."""
import argparse
from .core import ppm
from typing import Sequence


@ppm.regist_subcmd
def help(argv:Sequence[str]):
    """ppm help <subcommand>
ppm工具的子命令有:

    help              展示ppm的帮助说明
    version           展示ppm的版本
    template          管理模板
    project           管理项目
    stack             管理项目组
    proto             管理protobuffer文件
    doc               管理项目组文档
    docker            管理项目的docker操作           
    """
    parser = argparse.ArgumentParser(
        prog='ppm help',
        description='查看子命令的帮助说明',
        usage= ppm.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)

def cmd_help(args:argparse.Namespace):
    print(ppm.subcmds.get(args.subcmd).__doc__)