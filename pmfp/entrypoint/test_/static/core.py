from pmfp.utils.endpoint import EndPoint
from pmfp.utils.tools_info_utils import get_config_info
from ..core import test

pmfpinfo = get_config_info()


class Static(EndPoint):
    """对动态语言的源码做静态类型检验."""
    argparse_noflag = "code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["code", "language"],
        "properties": {
            "language": {
                "type": "string",
                "title": "l",
                "description": "静态类型检验针对的语言",
                "enum": ["py"]
            },
            "code": {
                "type": "string",
                "description": "指定要测的项目源码位置"
            },
            "output": {
                "type": "string",
                "title": "o",
                "description": "静态类型检验结果输出位置",
                "default": pmfpinfo.get("default_typecheck_doc_dir", "doc_typecheck")
            },
            "coverage": {
                "type": "boolean",
                "title": "v",
                "description": "静态类型检验是否输出覆盖率报告.",
                "default": False
            },
            "model": {
                "type": "boolean",
                "title": "m",
                "description": "静态类型检验针对的是否是模块",
                "default": False
            },
            "cwd": {
                "type": "string",
                "description": "静态类型检验执行的位置",
                "default": "."
            }
        }
    }


test_static = test.regist_sub(Static)
