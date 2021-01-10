from schema_entry import EntryPoint
from ..core import schema


class Move(EntryPoint):
    """迁移旧的json schema模式文件."""
    argparse_noflag = "file"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["file", "name", "to", "version"],
        "properties": {
            "file": {
                "type": "string",
                "description": "旧json schema的路径,如果路径指向一个文件夹则遍历文件夹执行相同的操作.",
            },
            "old_cwd": {
                "type": "string",
                "description": "旧schema的根目录地址.",
                "default": "."
            },
            "remove_old": {
                "type": "boolean",
                "description": "是否删除旧的json schema模式文件.",
            },
            "name": {
                "type": "string",
                "description": "模式名",
            },
            "addr": {
                "type": "string",
                "description": "网站域名"
            },
            "to": {
                "type": "string",
                "description": "从执行目录起的路径",
            },
            "version": {
                "type": "string",
                "description": "模式版本",
                "default": "0.0.0"
            },
            "cwd": {
                "type": "string",
                "description": "执行目录",
                "default": "."
            }
        }
    }


schema_move = schema.regist_sub(Move)
