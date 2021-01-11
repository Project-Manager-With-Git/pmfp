from schema_entry import EntryPoint
from ..core import test


class Static(EntryPoint):
    """对动态语言的源码做静态类型检验."""
    argparse_noflag = "code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["code", "language"],
        "properties": {
            "language": {
                "type": "string",
                "description": "静态类型检验针对的语言",
                "enum": ["py"]
            },
            "code": {
                "type": "string",
                "description": "指定要测的项目代码"
            },
            "output": {
                "type": "string",
                "description": "静态类型检验结果输出位置",
                "default": "doc_typecheck"
            },
            "coverage": {
                "type": "boolean",
                "description": "静态类型检验是否输出覆盖率报告."
            },
            "model": {
                "type": "boolean",
                "description": "静态类型检验针对的是否是模块",
            },
            "cwd": {
                "type": "string",
                "description": "静态类型检验执行的位置",
                "default": "."
            }
        }
    }


test_static = test.regist_sub(Static)
