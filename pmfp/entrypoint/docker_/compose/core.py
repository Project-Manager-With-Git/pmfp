"""ppm docker compose命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Compose(EntryPoint):
    """docker compose相关的工具."""


dockercompose = ppm.regist_sub(Compose)
