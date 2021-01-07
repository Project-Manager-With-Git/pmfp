"""ppm proto命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Proto(EntryPoint):
    """protobuf和grpc相关的工具."""


proto = ppm.regist_sub(Proto)
