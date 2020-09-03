"""ppm schema new命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_schema.cmd_schema_test import test_schema
from .core import ppm_schema


@ppm_schema.regist_subcmd
def test(argv: Sequence[str]) -> None:
    """检查schema文件中的`examples`是否符合定义.

    ppm schema test <file>

    这个schema文件可以是文件地址或者http/fiil的url
    """
    parser = argparse.ArgumentParser(
        prog='ppm schema test',
        description='检查json schema文件',
        usage=ppm_schema.subcmds.get("test").__doc__
    )
    parser.add_argument("file", type=str,
                        help="json schema文件")
    parser.set_defaults(func=cmd_test_schema)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_test_schema(args: argparse.Namespace) -> None:
    """检测schema."""
    test_schema(file=args.file)
