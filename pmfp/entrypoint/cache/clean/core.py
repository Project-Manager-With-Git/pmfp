"""ppm cache管理资源包缓存"""
from pmfp.utils.endpoint import EndPoint
from ..core import cache


class Clean(EndPoint):
    """清除所有资源包."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "title": "m",
                "description": "清除模式",
                "enum": ["all", "only_hash", "except_latest"],
                "default": "except_latest"
            },
            "host": {
                "type": "string",
                "description": "指定带删除的缓存的维护host",
            },
            "repo_namespace": {
                "type": "string",
                "title": "s",
                "description": "指定带删除的缓存命名空间"
            },
            "repo_name": {
                "type": "string",
                "title": "n",
                "description": "指定带删除的缓存仓库名,如果未指定则使用mode方式针对全部缓存"
            },
            "tags": {
                "type": "array",
                "title": "t",
                "description": "指定带删除的tag,如果不指定又有repo_name则删除全部",
                "items": {
                    "type": "string"
                }
            }
        }
    }


cache_clean = cache.regist_sub(Clean)
