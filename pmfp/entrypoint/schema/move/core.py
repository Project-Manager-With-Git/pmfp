from pmfp.utils.endpoint import EndPoint
from ..core import schema


class Move(EndPoint):
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
                "title": "o",
                "description": "旧schema的根目录地址.",
                "default": "."
            },
            "remove_old": {
                "type": "boolean",
                "title": "-r",
                "description": "是否删除旧的json schema模式文件.",
            },
            "name": {
                "type": "string",
                "title": "n",
                "description": "模式名",
            },
            "addr": {
                "type": "string",
                "title": "a",
                "description": "网站域名"
            },
            "to": {
                "type": "string",
                "title": "t",
                "description": "从执行目录起的路径",
            },
            "version": {
                "type": "string",
                "title": "v",
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
