"""ppm test static命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_test.cmd_test_static import static_test
from .core import ppm_test


@ppm_test.regist_subcmd
def static(argv: Sequence[str]) -> None:
    """对动态语言的源码做静态类型检验.

    ppm test static [-flags] model
    """
    parser = argparse.ArgumentParser(
        prog='ppm test static',
        description='对动态语言的源码做静态类型检验.',
        usage=ppm_test.subcmds.get("static").__doc__
    )
    parser.add_argument("-l", "--language", type=str,
                        choices=("py",), help="静态类型检验针对的语言.")
    parser.add_argument("-m", "--model", action="store_true",
                        help="静态类型检验针对是模块还是执行脚本.")
    parser.add_argument("-c", "--coverage", action="store_true",
                        help="静态类型检验是否输出覆盖率报告.")
    parser.add_argument("-o", "--output", type=str,
                        default="typecheck", help="静态类型检验结果输出位置.")
    parser.add_argument("code", type=str,
                        help="指定要测的项目代码")
    parser.set_defaults(func=cmd_static_test)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_static_test(args: argparse.Namespace) -> None:
    """检测动态语言的类型."""
    static_test(args.language, args.code, args.model, args.coverage, args.output)
