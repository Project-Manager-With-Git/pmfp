"""ppm test static命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_test.cmd_test_unittest import unittest_test
from .core import ppm_test


@ppm_test.regist_subcmd
def unittest(argv: Sequence[str]) -> None:
    """对指定语言的代码做单元测试.

    ppm test unittest [-flags] model
    """
    parser = argparse.ArgumentParser(
        prog='ppm test unittest',
        description='对指定语言的代码做单元测试.',
        usage=ppm_test.subcmds.get("unittest").__doc__
    )
    parser.add_argument("-l", "--language", type=str,required=True,
                        choices=("py","go"), help="单元测试针对的语言.")
    parser.add_argument("-c", "--coverage", action="store_true",
                        help="单元测试是否输出覆盖率报告.")
    parser.add_argument("-s", "--source", type=str,nargs="+",
                        help="单元测试覆盖的源码范围.")
    parser.add_argument("-o", "--output", type=str,
                        default="typecheck", help="单元测试结果输出位置.")
    parser.add_argument("-t","--testcode", type=str,default=".",
                        help="指定要测的测试代码")
    parser.set_defaults(func=cmd_unittest_test)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_unittest_test(args: argparse.Namespace) -> None:
    """检测动态语言的类型."""
    unittest_test(language=args.language,testcode=args.testcode,source=args.source, coverage=args.coverage, output=args.output)
