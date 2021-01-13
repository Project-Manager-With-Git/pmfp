from schema_entry import EntryPoint
from ..core import doc


class Build(EntryPoint):
    """为指定编程语言编译api文档."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["language"],
        "properties": {
            "language": {
                "type": "string",
                "description": "单元测试检验针对的语言",
                "enum": ["py"]
            },
            "output": {
                "type": "string",
                "description": "html文档位置",
                "default": "doc"
            },
            "source_dir": {
                "type": "string",
                "description": "文档源码位置",
                "default": "document"
            },
            "version": {
                "type": "string",
                "description": "文档源码位置"
            },
            "cwd": {
                "type": "string",
                "description": "执行的位置",
                "default": "."
            }
        }
    }


doc_build = doc.regist_sub(Build)
