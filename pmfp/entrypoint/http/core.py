"""ppm http命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Http(EntryPoint):
    """http相关的子命令."""


http = ppm.regist_sub(Http)
