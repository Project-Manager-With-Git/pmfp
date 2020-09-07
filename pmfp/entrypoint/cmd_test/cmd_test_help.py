"""ppm test help命令的处理."""
import argparse
from typing import Sequence
from .core import ppm_test


@ppm_test.regist_subcmd
def help(argv: Sequence[str]) -> None:
    """子命令ppm test的帮助信息.

    ppm test <subcmd>

    ppm test 的子命令有:

    unittest            执行代码单元测试
    benchmark           执行代码性能测试
    static              执行代码静态类型检验
    """
    parser = argparse.ArgumentParser(
        prog='ppm test help',
        description='查看子命令的帮助说明',
        usage=ppm_test.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_test.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_help(args: argparse.Namespace) -> None:
    """Test help."""
    print(ppm_test.subcmds.get(args.subcmd).__doc__)
