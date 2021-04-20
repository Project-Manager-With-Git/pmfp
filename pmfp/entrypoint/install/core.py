"""ppm install命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import ppm


class Install(EndPoint):
    """为执行环境安装依赖."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["env"],
        "properties": {
            "env": {
                "description": "静态类型检验针对的语言",
                "title": "e",
                "type": "string",
                "enum": ["venv", "conda", "gomod"]
            },
            "requires": {
                "type": "array",
                "title": "r",
                "description": "最小化执行的依赖",
                "items": {
                    "type": "string"
                }
            },
            "test_requires": {
                "type": "array",
                "title": "t",
                "description": "开发测试时的依赖",
                "items": {
                    "type": "string"
                }
            },
            "setup_requires": {
                "type": "array",
                "title": "s",
                "description": "安装时的依赖",
                "items": {
                    "type": "string"
                }
            },
            "extras_requires": {
                "type": "array",
                "title": "",
                "description": "扩展的依赖",
                "items": {
                    "type": "string"
                }
            },
            "cwd": {
                "type": "string",
                "description": "执行指令的位置",
                "default": "."
            }
        }
    }


install = ppm.regist_sub(Install)
