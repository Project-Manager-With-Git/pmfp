"""ppm cache管理资源包缓存"""
from pmfp.utils.endpoint import EndPoint
from ..core import ppm


class Cache(EndPoint):
    """资源包缓存相关命令."""


cache = ppm.regist_sub(Cache)
