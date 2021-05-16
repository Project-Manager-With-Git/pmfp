"""ppm requires install命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import requires
from ...core import ppm


class Install(EndPoint):
    """为执行环境安装依赖.

    当指定package_names或者requirements时作为单独安装,否则作为批处理.

    当单独安装时test,setup,extras用于指示作为什么进行安装,优先级为test->setup->extras->requires
    当作为批处理时则使用test,setup,extras用于指示除了requires外需要安装的部分.此时extras的值不会使用到
    """
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["env"],
        "properties": {
            "env": {
                "description": "静态类型检验针对的语言",
                "type": "string",
                "enum": ["venv", "conda", "gomod", "node"]
            },
            "package_names": {
                "type": "array",
                "title": "n",
                "description": "要安装的包名",
                "items": {
                    "type": "string"
                }
            },
            "requirements": {
                "type": "string",
                "title": "r",
                "description": "指定`requirements.txt路径`",
            },
            "test": {
                "type": "boolean",
                "title": "t",
                "description": "package_names存在时安装包为测试依赖,否则只安装测试依赖",
                "default": False
            },
            "setup": {
                "type": "boolean",
                "title": "s",
                "description": "package_names存在时安装包为setup依赖,否则只安装setup依赖",
                "default": False
            },
            "extras": {
                "type": "string",
                "title": "x",
                "description": "package_names存在时安装包为指定key的extras依赖,否则只安装extras依赖",
            },
            "requires": {
                "type": "array",
                "description": "最小化执行的依赖,package_names不存在时生效",
                "items": {
                    "type": "string"
                }
            },
            "test_requires": {
                "type": "array",
                "description": "开发测试时的依赖,package_names不存在时生效",
                "items": {
                    "type": "string"
                }
            },
            "setup_requires": {
                "type": "array",
                "description": "安装时的依赖,package_names不存在时生效",
                "items": {
                    "type": "string"
                }
            },
            "extras_requires": {
                "type": "array",
                "description": "扩展的依赖,package_names不存在时生效",
                "items": {
                    "type": "string"
                }
            },
            "env_args": {
                "type": "array",
                "title": "e",
                "description": "执行指令时的环境变量,<key::value>",
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


requires_install = requires.regist_sub(Install)
ppm_install = ppm.regist_sub(Install)
