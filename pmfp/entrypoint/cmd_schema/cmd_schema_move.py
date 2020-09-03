"""ppm schema move命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_schema.cmd_schema_move import move_schema
from .core import ppm_schema


@ppm_schema.regist_subcmd
def move(argv: Sequence[str]) -> None:
    """迁移旧的json schema模式文件.

    ppm schema move [-flags] <name>

    模式文件将以存放路径或者网址路径作为id
    """
    parser = argparse.ArgumentParser(
        prog='ppm schema move',
        description='迁移json schema文件',
        usage=ppm_schema.subcmds.get("move").__doc__
    )
    parser.add_argument("-p", "--path", type=str,
                        help="相对根目录的路径")
    parser.add_argument("-v", "--version", type=str,
                        help="模式的版本")
    parser.add_argument("-r", "--root", type=str,
                        help="存放的根地址")
    parser.add_argument("-a", "--addr", type=str,
                        help="网址")
    parser.add_argument("-n", "--name", type=str,
                        help="schema名")
    parser.add_argument("--remove_old", action="store_true",
                        help="是否删除旧的json schema模式文件")
    parser.add_argument('-o', "--old_root", type=str, required=True,
                        help="旧schema的根目录地址")
    parser.add_argument("file", type=str,
                        help="旧json schema的路径,如果路径指向一个文件夹则遍历文件夹执行相同的操作.")
    parser.set_defaults(func=cmd_move_schema)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_move_schema(args: argparse.Namespace) -> None:
    """迁移schema."""
    move_schema(
        file=args.file,
        old_root=args.old_root,
        remove_old=args.remove_old,
        name=args.name,
        path=args.path,
        version=args.version,
        root=args.root,
        addr=args.addr)
