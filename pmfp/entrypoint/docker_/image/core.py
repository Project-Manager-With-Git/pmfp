
"""ppm docker image命令的处理."""
from schema_entry import EntryPoint
from ..core import docker


class Image(EntryPoint):
    """docker image相关的工具."""


dockerimage = docker.regist_sub(Image)
