"""version命令的处理."""
from typing import Sequence
from pmfp import VERSION
from .core import ppm


@ppm.regist_subcmd
def version(argv: Sequence[str]) -> None:
    """获取pmfp工具的版本.

    ppm version
    """
    cmd_version()


def cmd_version() -> None:
    """打印工具的版本."""
    print(VERSION)
