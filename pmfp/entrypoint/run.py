"""run命令的处理."""
from pathlib import Path
from typing import Optional, Any

from schema_entry import EntryPoint
from pmfp.utils.run_command_utils import run_command
from .core import ppm


class RUN(EntryPoint):
    """执行命令行操作."""

    argparse_noflag = "files"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["commands"],
        "properties": {
            "commands": {
                "description": "要执行的命令",
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "env": {
                "type": "boolean",
                "description": "是否是grpc",
                "default": False
            },
            "cwd": {
                "type": "string",
                "description": "存放的地方",
                "default": "."
            }
        }
    }


run = ppm.regist_sub(RUN)


@run.as_main
def run_cmd(command: str, *, cwd: str = ".", env: Optional[Any] = None):
    run_command(command, cwd=Path(cwd), env=env, visible=True).get()
