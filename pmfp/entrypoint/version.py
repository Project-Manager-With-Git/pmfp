"""version命令的处理."""
import json
import configparser
from pathlib import Path
from schema_entry import EntryPoint
from .core import ppm

__VERSION__ = "4.0.7"


class VERSION(EntryPoint):
    """获取pmfp工具的版本."""
    verify_schema = False

    def do_main(self) -> None:
        print(f"pmfp version: {__VERSION__}")


version = ppm.regist_sub(VERSION)
