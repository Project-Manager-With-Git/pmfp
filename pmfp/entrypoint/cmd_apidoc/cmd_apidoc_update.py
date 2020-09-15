"""ppm apidoc new命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_apidoc.cmd_apidoc_update import update_apidoc
from .core import ppm_apidoc
from pmfp.const import DEFAULT_AUTHOR


@ppm_apidoc.regist_subcmd
def update(argv: Sequence[str]) -> None:
    """为指定编程语言构造api文档.

    ppm apidoc update [-flags] code
    """
    parser = argparse.ArgumentParser(
        prog='ppm apidoc build',
        description='为指定编程语言构造api文档.',
        usage=ppm_apidoc.subcmds.get("update").__doc__
    )
    parser.add_argument("-l", "--language", type=str, required=True,
                        choices=("py"), help="指定编程语言.")
    parser.add_argument("--root", type=str, default=".",
                        help="指定要覆盖的项目根目录")
    parser.add_argument("-s", "--source_dir", type=str,
                        default="document", help="文档源文件的输出位置")
    parser.add_argument("-o", "--output", type=str,
                        default="docs", help="文档静态html文件的输出位置")
    parser.add_argument("code", type=str,
                        help="指定要覆盖的代码位置")
    parser.set_defaults(func=cmd_update_apidoc)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_update_apidoc(args: argparse.Namespace) -> None:
    """检测动态语言的类型."""
    update_apidoc(
        language=args.language,
        output=args.output,
        source_dir=args.source_dir,
        code=args.code,
        root=args.root
    )
