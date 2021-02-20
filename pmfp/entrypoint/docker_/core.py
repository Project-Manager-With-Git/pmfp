"""ppm docker命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Docker(EntryPoint):
    """docker相关的工具."""


docker = ppm.regist_sub(Docker)
