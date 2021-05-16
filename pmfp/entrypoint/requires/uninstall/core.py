"""ppm requires uninstall命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import requires
from ...core import ppm


class Uninstall(EndPoint):
    """为执行环境卸载依赖."""
    argparse_noflag = "package_name"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["env"],
        "properties": {
            "package_name": {
                "type": "string",
                "description": "要卸载的包名",
            },
            "env": {
                "description": "静态类型检验针对的语言",
                "type": "string",
                "enum": ["venv", "conda"]
            },
            "cwd": {
                "type": "string",
                "description": "执行指令的位置",
                "default": "."
            }
        }
    }


requires_uninstall = requires.regist_sub(Uninstall)
ppm_uninstall = ppm.regist_sub(Uninstall)
