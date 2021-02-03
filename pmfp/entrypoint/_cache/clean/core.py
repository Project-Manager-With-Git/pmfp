"""ppm cache管理资源包缓存"""
from pmfp.utils.endpoint import EndPoint
from ..core import cache


class Clean(EndPoint):
    """清除所有资源包."""


cache_clean = cache.regist_sub(Clean)
