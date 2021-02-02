"""ppm cache管理资源包缓存"""
from schema_entry import EntryPoint
from ..core import cache


class Clean(EntryPoint):
    """清除所有资源包."""


cache_clean = cache.regist_sub(Clean)
