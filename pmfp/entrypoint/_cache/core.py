"""ppm cache管理资源包缓存"""
from schema_entry import EntryPoint
from ..core import ppm


class Cache(EntryPoint):
    """编译指定位置项目."""
    
cache_cmd = ppm.regist_sub(Cache)
