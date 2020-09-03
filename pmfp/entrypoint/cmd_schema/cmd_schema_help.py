"""ppm schema help命令的处理."""
import argparse
from typing import Sequence
from .core import ppm_schema


@ppm_schema.regist_subcmd
def help(argv: Sequence[str]) -> None:
    """子命令ppm schema的帮助信息.

    ppm schema help <subcommand>

    ppm schema工具的子命令有:

        new                 创建一个json schema的模式文件
        move                将一个存在的json schema模式文件改变位置并更改id.
        check               检查一个json文件是否满足指定的json schema的模式
        test                检查一个json schema的模式文件中的样例是否满足该模式
    """
    parser = argparse.ArgumentParser(
        prog='ppm schema help',
        description='查看子命令的帮助说明',
        usage=ppm_schema.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_schema.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_help(args: argparse.Namespace) -> None:
    """Schema help."""
    print(ppm_schema.subcmds.get(args.subcmd).__doc__)
