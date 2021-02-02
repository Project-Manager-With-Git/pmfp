from schema_entry import EntryPoint
from ..core import cache


class Get(EntryPoint):
    """从远端获取模板仓库到本地缓存."""
    argparse_noflag = "source_pack_string"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["source_pack_string"],
        "properties": {
            "source_pack_string": {
                "type": "string",
                "description": "资源包路径",
            }
        }
    }


cache_get = cache.regist_sub(Get)
