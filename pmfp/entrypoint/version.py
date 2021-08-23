"""version命令的处理."""
from schema_entry import EntryPoint
from .core import ppm

__VERSION__ = "4.1.3"


class VERSION(EntryPoint):
    """获取pmfp工具的版本."""
    verify_schema = False

    def do_main(self) -> None:
        print(f"pmfp version: {__VERSION__}")


version = ppm.regist_sub(VERSION)

__all__ = ["__VERSION__"]
