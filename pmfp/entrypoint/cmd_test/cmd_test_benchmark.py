"""ppm test static命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_test.cmd_test_benchmark import benchmark_test
from .core import ppm_test


@ppm_test.regist_subcmd
def benchmark(argv: Sequence[str]) -> None:
    """对指定语言的代码做性能测试.

    ppm test benchmark [-flags] model
    """
    parser = argparse.ArgumentParser(
        prog='ppm test benchmark',
        description='对指定语言的代码做性能测试.',
        usage=ppm_test.subcmds.get("benchmark").__doc__
    )
    parser.add_argument("-l", "--language", type=str,required=True,
                        choices=("py","go"), help="性能测试针对的语言.")
    parser.add_argument("-t","--testcode", type=str,default=".",
                        help="指定要测的测试代码")
    parser.add_argument("--mem",type=str,action="store_true",
                        help="指定时否是要测试内存占用,如果否则执行cpu性能测试.")
    parser.set_defaults(func=cmd_benchmark_test)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_benchmark_test(args: argparse.Namespace) -> None:
    """检测动态语言的类型."""
    benchmark_test(language=args.language,testcode=args.testcode,mem=args.mem)
