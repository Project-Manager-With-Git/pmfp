from pmfp.utils.endpoint import EndPoint
from ..core import doc


class Build(EndPoint):
    """为指定编程语言编译api文档."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["language"],
        "properties": {
            "language": {
                "type": "string",
                "title": "l",
                "description": "文档针对的语言",
                "enum": ["py"]
            },
            "output": {
                "type": "string",
                "title": "o",
                "description": "html文档位置",
                "default": "docs"
            },
            "doc_source_dir": {
                "type": "string",
                "description": "文档源码位置",
                "default": "document"
            },
            "version": {
                "type": "string",
                "title": "v",
                "description": "项目版本"
            },
            "cwd": {
                "type": "string",
                "description": "执行的位置",
                "default": "."
            }
        }
    }


doc_build = doc.regist_sub(Build)
