"""ppm docker compose命令的处理."""
from schema_entry import EntryPoint
from ..core import docker


class Compose(EntryPoint):
    """docker compose相关的工具."""


dockercompose = docker.regist_sub(Compose)
