"""ppm build命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import ppm


class Build(EndPoint):
    """编译指定位置项目."""
    argparse_noflag = "code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["code", "project_name"],
        "properties": {
            "language": {
                "type": "string",
                "title": "l",
                "description": "编译的代码语言",
                "enum": ["go"]
            },
            "code": {
                "description": "语言源码位置或者入口文件位置",
                "type": "string",
            },
            "output_dir": {
                "type": "string",
                "title": "t",
                "description": "编译结果目录",
                "default": "."
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "项目名"
            },
            "upx": {
                "type": "boolean",
                "title": "u",
                "description": "是否使用upx给可执行文件加壳"
            },
            "static": {
                "type": "boolean",
                "title": "s",
                "description": "是否编译为无依赖的静态文件",
                "default": True
            },
            "mini": {
                "type": "boolean",
                "title": "m",
                "description": "是否最小化编译"
            },
            "includes": {
                "type": "array",
                "title": "i",
                "description": "包含的头文件路径",
                "items": {
                    "type": "string"
                }
            },
            "libs": {
                "type": "array",
                "title": "b",
                "description": "使用的库名",
                "items": {
                    "type": "string"
                }
            },
            "lib_dir": {
                "type": "array",
                "title": "d",
                "description": "使用的库的位置",
                "items": {
                    "type": "string"
                }
            },
            "build_as": {
                "type": "string",
                "title": "a",
                "description": "编译为的目标,可选有exec,alib,dlib",
                "enum": ["exec", "alib", "dlib"],
                "default": "exec"
            },
            "for_linux_arch": {
                "type": "string",
                "title": "f",
                "description": "是否交叉编译支持其他指令集版本的linux",
                "enum": ["arm64", "amd64"]
            },
            "cwd": {
                "type": "string",
                "description": "执行编译操作时的执行位置",
                "default": "."
            }
        }
    }


build_cmd = ppm.regist_sub(Build)
