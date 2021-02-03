from schema_entry import EntryPoint
from ..core import env


class New(EntryPoint):
    """在目标文件夹构造执行环境."""
    argparse_noflag = "env"
    default_config_file_paths = ["./ppmrc.json"]
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["env"],
        "properties": {
            "env": {
                "description": "静态类型检验针对的语言",
                "title": "e",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["venv", "conda", "gomod"]
                }
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
            "cwd": {
                "type": "string",
                "description": "静态类型检验执行的位置",
                "default": "."
            }
        }
    }


env_new = env.regist_sub(New)
