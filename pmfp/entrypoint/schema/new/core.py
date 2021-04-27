from pmfp.utils.endpoint import EndPoint
from ..core import schema


class New(EndPoint):
    """创建一个json schema 模板."""
    argparse_noflag = "name"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["name", "to", "version"],
        "properties": {
            "name": {
                "type": "string",
                "description": "模式名",
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
            "addr": {
                "type": "string",
                "title": "a",
                "description": "网站域名"
            },
            "cwd": {
                "type": "string",
                "description": "执行目录",
                "default": "."
            }
        }
    }


schema_new = schema.regist_sub(New)
