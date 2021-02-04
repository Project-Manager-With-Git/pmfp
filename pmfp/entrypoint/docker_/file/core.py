"""ppm test命令的处理."""
from schema_entry import EntryPoint
from ..core import docker


class File(EntryPoint):
    """dockerfile相关的工具."""


dockerfile = docker.regist_sub(File)
