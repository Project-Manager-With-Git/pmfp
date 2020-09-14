"""ppm apidoc new命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_apidoc.cmd_apidoc_new import new_apidoc
from .core import ppm_apidoc
from pmfp.const import DEFAULT_AUTHOR


@ppm_apidoc.regist_subcmd
def new(argv: Sequence[str]) -> None:
    """为指定编程语言构造api文档.

    ppm apidoc new [-flags] code
    """
    parser = argparse.ArgumentParser(
        prog='ppm apidoc new',
        description='为指定编程语言构造api文档.',
        usage=ppm_apidoc.subcmds.get("new").__doc__
    )
    parser.add_argument("-l", "--language", type=str,required=True,
                        choices=("py"), help="指定编程语言.")
    parser.add_argument("--root",type=str,default=".",
                        help="指定要覆盖的项目根目录")
    parser.add_argument("-n","--project_name",type=str,
                        default="example",help="项目名")
    parser.add_argument("-a","--author",type=str,
                        default=DEFAULT_AUTHOR,help="项目作者")
    parser.add_argument("-v","--version",type=str,
                        default="0.0.0",help="项目版本")
    parser.add_argument("-s","--source_dir",type=str,
                        default="document",help="文档源文件的输出位置")  
    parser.add_argument("-o", "--output", type=str,
                        default="docs", help="文档静态html文件的输出位置")
    parser.add_argument("code",type=str,
                        help="指定要覆盖的代码对根目录的相对位置")
    parser.set_defaults(func=cmd_new_apidoc)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_new_apidoc(args: argparse.Namespace) -> None:
    """检测动态语言的类型."""
    new_apidoc(
        language=args.language,
        project_name=args.project_name,
        author=args.author, 
        version=args.version, 
        output=args.output,
        source_dir=args.source_dir,
        code=args.code,
        root=args.root)
