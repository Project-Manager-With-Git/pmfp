"""ppm test命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import project


class New(EndPoint):
    """根据模板创建项目."""

    argparse_noflag = "env"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["env"],
        "properties": {
            "env": {
                "description": "执行环境",
                "title": "e",
                "type": "string",
                "enum": ["venv", "conda", "gomod", "cmake"]
            },
            "language": {
                "type": "string",
                "title": "l",
                "description": "初始化的语言",
                "enum": ["py", "cython", "go", "CXX", "C"]
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "项目名"
            },
            "author": {
                "type": "string",
                "title": "a",
                "description": "项目作者"
            },
            "author_email": {
                "type": "string",
                "title": "m",
                "description": "作者email"
            },
            "version": {
                "type": "string",
                "title": "v",
                "description": "项目版本"
            },
            "description": {
                "type": "string",
                "title": "d",
                "description": "项目简介"
            },
            "keywords": {
                "description": "关键字",
                "title": "k",
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "requires": {
                "type": "array",
                "title": "r",
                "description": "最小化执行的依赖",
                "items": {
                    "type": "string"
                }
            },
            "template_string": {
                "type": "string",
                "title": "t",
                "description": "使用的模板"
            },
            "install": {
                "type": "boolean",
                "title": "i",
                "description": "是否安装依赖",
                "default": False
            },
            "cwd": {
                "type": "string",
                "description": "执行指令的位置",
                "default": "."
            }
        }
    }


project_new = project.regist_sub(New)
