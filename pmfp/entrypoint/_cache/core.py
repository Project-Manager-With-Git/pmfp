"""ppm cache管理资源包缓存"""
from schema_entry import EntryPoint
from ..core import ppm


class Cache(EntryPoint):
    """资源包缓存相关命令."""


cache = ppm.regist_sub(Cache)
