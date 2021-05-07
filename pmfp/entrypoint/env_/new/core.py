from pmfp.utils.endpoint import EndPoint
from ..core import env


class New(EndPoint):
    """在目标文件夹构造执行环境."""
    argparse_noflag = "language"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["language"],
        "properties": {
            "env": {
                "description": "执行环境",
                "title": "e",
                "type": "string",
                "enum": ["venv", "conda", "pypy", "gomod", "cmake", "node", "webpack", "http"]
            },
            "language": {
                "type": "string",
                "title": "l",
                "description": "初始化的语言",
                "enum": ["py", "cython", "go", "CXX", "C", "js", "md"]
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
                "description": "最小化执行的依赖",
                "items": {
                    "type": "string"
                }
            },
            "test_requires": {
                "type": "array",
                "description": "开发测试时的依赖",
                "items": {
                    "type": "string"
                }
            },
            "setup_requires": {
                "type": "array",
                "description": "安装时的依赖",
                "items": {
                    "type": "string"
                }
            },
            "extras_requires": {
                "type": "array",
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


env_new = env.regist_sub(New)
