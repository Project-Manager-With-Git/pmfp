from pmfp.utils.endpoint import EndPoint
from ..core import doc


class New(EndPoint):
    """为指定编程语言构造api文档.
    如果不指定项目名则项目名为cwd目录名,不指定version则为0.0.0,不指定author则为系统用户.
    """
    argparse_noflag = "code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["code", "language"],
        "properties": {
            "language": {
                "type": "string",
                "title": "l",
                "description": "单元测试检验针对的语言",
                "enum": ["py", "go"]
            },
            "code": {
                "type": "string",
                "description": "指定项目源码位置"
            },
            "output": {
                "type": "string",
                "title": "o",
                "description": "html文档位置",
                "default": "docs"
            },
            "doc_source_dir": {
                "type": "string",
                "title": "s",
                "description": "文档源码位置",
                "default": "document"
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "文档源码位置"
            },
            "author": {
                "type": "string",
                "title": "a",
                "description": "文档源码位置"
            },
            "version": {
                "type": "string",
                "title": "v",
                "description": "文档源码位置"
            },
            "cwd": {
                "type": "string",
                "description": "执行的位置",
                "default": "."
            }
        }
    }


doc_new = doc.regist_sub(New)
