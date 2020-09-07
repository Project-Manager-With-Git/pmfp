"""ppm cache help命令的处理."""
import argparse
from .core import ppm_cache
from typing import Sequence


@ppm_cache.regist_subcmd
def help(argv: Sequence[str]) -> None:
    """子命令ppm cache的帮助信息.

    ppm cache help <subcommand>

    管理资源包缓存
    ppm cache 的子命令有:

    get                  获取资源包放入缓存
    clean                清除所有资源包缓存  

    """
    parser = argparse.ArgumentParser(
        prog='ppm cache help',
        description='查看子命令的帮助说明',
        usage=ppm_cache.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_cache.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_help(args: argparse.Namespace) -> None:
    """cache Help."""
    print(ppm_cache.subcmds.get(args.subcmd).__doc__)
