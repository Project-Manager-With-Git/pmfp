"""reset命令的处理."""
import argparse
from pathlib import Path
from typing import Sequence
from pmfp.features.cmd_env.cmd_env import new_env
from .core import ppm


@ppm.regist_subcmd
def env(argv: Sequence[str]) -> None:
    """执行命令行操作.

    ppm env <env>
    """
    parser = argparse.ArgumentParser(
        prog='ppm env',
        description='指定地址构造执行环境',
        usage=ppm.subcmds.get("env").__doc__
    )
    parser.add_argument("--root", type=str, default=".", help="创建环境的位置")
    parser.add_argument("--project_name", type=str, default="example", help="环境对应的项目名")
    parser.add_argument("--project_version", type=str, default="0.0.0", help="环境对应的项目版本")
    parser.add_argument("--project_license", type=str, default="MIT", help="环境对应的项目的协议")
    parser.add_argument("--author", type=str, default="", help="环境对应的项目的作者")
    parser.add_argument("--author-email", type=str, default="MIT", help="环境对应的项目的作者email")
    parser.add_argument("--keywords", type=str, default="MIT", help="环境对应的项目的关键字")
    parser.add_argument("--description", type=str, default="MIT", help="环境对应的项目的说明")
    parser.add_argument("env", type=str, choices=("py","conda","js","vue","go"), help="初始化的环境")
    parser.set_defaults(func=cmd_env)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_env(args: argparse.Namespace) -> None:
    new_env()