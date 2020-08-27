"""ppm schema new命令的处理."""
import argparse
from .core import ppm_schema
from typing import Sequence
from pmfp.features.cmd_schema.cmd_schema_new import new_schema


@ppm_schema.regist_subcmd
def new(argv:Sequence[str]):
    """ppm schema new [-flags] <name>

    创建新的json schema模式文件.
    模式文件将以存放路径或者网址路径作为id
    """
    parser = argparse.ArgumentParser(
        prog='ppm schema new',
        description='创建json schema文件',
        usage= ppm_schema.subcmds.get("new").__doc__
    )
    parser.add_argument("-p", "--path", type=str,default=".", help="相对根目录的路径")
    parser.add_argument("-v", "--version", type=str,default="v0.0.0", help="模式的版本")
    parser.add_argument("-r", "--root", type=str,default=".", help="存放的根地址") 
    parser.add_argument("-a", "--addr", type=str, help="网址") 
    parser.add_argument("name",type=str, help="schema名")
    parser.set_defaults(func=cmd_new_schema)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_new_schema(args: argparse.Namespace):
    new_schema(name=args.name,path=args.path,version=args.version,root=args.root,addr=args.addr)
