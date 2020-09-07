"""ppm cache get命令的处理."""
import argparse
from typing import Sequence
from pmfp.features.cmd_cache.cmd_cache_clean import sourcepack_clean
from .core import ppm_cache


@ppm_cache.regist_subcmd
def clean(_: Sequence[str]) -> None:
    """展示目前缓存了哪些资源包.

    ppm cache clean
    """
    sourcepack_clean()
   



