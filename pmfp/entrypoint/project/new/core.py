"""ppm test命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import project


class New(EndPoint):
    """根据模板创建项目."""

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
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
            "template_string": {
                "type": "string",
                "title": "t",
                "description": "使用的模板的描述字符串,形式为[[{host}::]{repo_namespace}::]{repo_name}[@{tag}]"
            },
            "with_test": {
                "type": "boolean",
                "description": "是否安装依赖",
                "default": False
            },
            "install": {
                "type": "boolean",
                "title": "i",
                "description": "是否安装依赖",
                "default": False
            },
            "install_env_args": {
                "type": "array",
                "description": "执行指令时的环境变量,<key::value>",
                "items": {
                    "type": "string"
                }
            },
            "kv": {
                "type": "array",
                "description": "替换模板的默认参数,格式为`<key>::<value>`",
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


project_new = project.regist_sub(New)
