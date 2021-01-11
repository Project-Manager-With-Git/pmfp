from schema_entry import EntryPoint
from ..core import test


class Unittest(EntryPoint):
    """对源码做单元测试."""
    argparse_noflag = "code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["code", "language"],
        "properties": {
            "language": {
                "type": "string",
                "description": "静态类型检验针对的语言",
                "enum": ["py", "go"]
            },
            "code": {
                "type": "string",
                "description": "指定要测的项目代码"
            },
            "output": {
                "type": "string",
                "description": "静态类型检验结果输出位置",
                "default": "typecheck"
            },
            "coverage": {
                "type": "boolean",
                "description": "静态类型检验是否输出覆盖率报告."
            },
            "source": {
                "type": "string",
                "description": "测试覆盖代码",
            },
            "cwd": {
                "type": "string",
                "description": "静态类型检验执行的位置",
                "default": "."
            }
        }
    }


test_unittest = test.regist_sub(Unittest)
