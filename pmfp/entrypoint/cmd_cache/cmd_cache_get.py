"""ppm cache get命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_cache.cmd_cache_get import get_sourcepack
from .core import ppm_cache


@ppm_cache.regist_subcmd
def get(argv: Sequence[str]) -> None:
    """根据资源包字符串获取资源包并缓存.

    ppm cache get <source_pack_string>
    """
    parser = argparse.ArgumentParser(
        prog='ppm cache get',
        description='缓存资源包',
        usage=ppm_cache.subcmds.get("get").__doc__
    )

    parser.add_argument("source_pack_string", type=str,
                        help="资源包描述字符串")
    parser.set_defaults(func=cmd_get_cache)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_get_cache(args: argparse.Namespace) -> None:
    """新建一个protobuf."""
    get_sourcepack(source_pack_string=args.source_pack_string)
