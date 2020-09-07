"""ppm project help命令的处理."""
import argparse
from .core import ppm_project
from typing import Sequence


@ppm_project.regist_subcmd
def help(argv: Sequence[str]) -> None:
    """子命令ppm project的帮助信息.

    ppm project help <subcommand>

    ppm project工具的子命令有:

        init              初始化一个项目.
        add               新增组件
        info              查看项目信息
        update            更新项目
        build             编译项目
        upload            上传项目
        release           发布项目
        clean             清除一个项目
        test              执行测试
        doc               编译文档
    """
    parser = argparse.ArgumentParser(
        prog='ppm project help',
        description='查看子命令的帮助说明',
        usage=ppm_project.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_project.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_help(args: argparse.Namespace) -> None:
    """Project Help."""
    print(ppm_project.subcmds.get(args.subcmd).__doc__)
