"""ppm apidoc help命令的处理."""
import argparse
from typing import Sequence
from .core import ppm_apidoc


@ppm_apidoc.regist_subcmd
def help(argv: Sequence[str]) -> None:
    """子命令ppm apidoc的帮助信息.

    ppm apidoc 的子命令有:

    new             为项目创建一个api文档
    update          更新api文档
    newlocale       新增小语种支持
    build           编译文档源文件为html静态页面
    """
    parser = argparse.ArgumentParser(
        prog='ppm apidoc help',
        description='查看子命令的帮助说明',
        usage=ppm_apidoc.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_apidoc.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_help(args: argparse.Namespace) -> None:
    """Apidoc help."""
    print(ppm_apidoc.subcmds.get(args.subcmd).__doc__)
