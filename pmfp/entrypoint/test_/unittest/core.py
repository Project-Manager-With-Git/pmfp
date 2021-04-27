from pmfp.utils.endpoint import EndPoint
from pmfp.utils.tools_info_utils import get_config_info
from ..core import test

pmfpinfo = get_config_info()


class Unittest(EndPoint):
    """对源码做单元测试.

    单元测试的覆盖率会放到指定位置.
    """
    argparse_noflag = "test_code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["code", "language", "test_code"],
        "properties": {
            "language": {
                "type": "string",
                "title": "l",
                "description": "单元测试检验针对的语言",
                "enum": ["py", "go"]
            },
            "code": {
                "type": "string",
                "title": "s",
                "description": "指定要测的项目源码"
            },
            "output": {
                "type": "string",
                "title": "o",
                "description": "单元测试检验结果输出位置",
                "default": pmfpinfo.get("default_unittest_doc_dir", "doc_unittest")
            },
            "coverage": {
                "title": "v",
                "type": "boolean",
                "description": "单元测试检验是否输出覆盖率报告."
            },
            "test_code": {
                "type": "string",
                "description": "测试代码",
            },
            "cwd": {
                "type": "string",
                "description": "单元测试检验执行的位置",
                "default": "."
            }
        }
    }


test_unittest = test.regist_sub(Unittest)
