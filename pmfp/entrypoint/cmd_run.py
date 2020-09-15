"""reset命令的处理."""
import argparse
from pathlib import Path
from typing import Sequence, Optional, Dict
from pmfp.utils.run_command_utils import run_command
from .core import ppm


@ppm.regist_subcmd
def run(argv: Sequence[str]) -> None:
    """执行命令行操作.

    ppm run <commands>
    """
    parser = argparse.ArgumentParser(
        prog='ppm reset',
        description='重置pmfp的配置',
        usage=ppm.subcmds.get("reset").__doc__
    )
    parser.add_argument("--cwd", type=str, help="执行命令的根目录")
    parser.add_argument("--env", type=str, help="执行命令时指定环境变量,用key1:value1;key2:value2的形式指定")
    parser.add_argument("commands", type=str, nargs="+", help="要执行的命令")
    parser.set_defaults(func=cmd_run)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_run(args: argparse.Namespace) -> None:
    """重置pmfp工具的配置."""
    cwd: Optional[Path]
    env: Optional[Dict[str, str]]
    command = " ".join(args.commands)

    if args.cwd:
        cwd = Path(args.cwd).resolve()
    else:
        cwd = None
    if args.env:
        env = dict([pair.split(":") for pair in args.env.split(";")])
    else:
        env = None
    run_command(command=command, cwd=cwd, env=env)
