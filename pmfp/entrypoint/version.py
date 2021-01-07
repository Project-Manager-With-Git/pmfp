"""version命令的处理."""
import json
import configparser
from pathlib import Path
from schema_entry import EntryPoint
from .core import ppm

__VERSION__ = "4.0.0"


class VERSION(EntryPoint):
    """获取pmfp工具的版本."""
    verify_schema = False


version = ppm.regist_sub(VERSION)


@version.as_main
def cmd_version() -> None:
    """打印工具的版本."""
    print(f"pmfp version: {__VERSION__}")
