"""run命令的处理."""
import os
from pathlib import Path
from typing import Optional, List, Dict

from schema_entry import EntryPoint
from pmfp.utils.run_command_utils import run as run_command
from .core import ppm


class RUN(EntryPoint):
    """执行命令行操作."""

    argparse_noflag = "files"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["command"],
        "properties": {
            "command": {
                "description": "要执行的命令,可以是形式为列表的字符串,会被解析为列表",
                "type": "string"
            },
            "env_args": {
                "type": "array",
                "description": "执行命令时的环境变量",
                "items": {
                    "type": "string"
                }
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
def run_cmd(command: str, *, cwd: str = ".", env_args: Optional[List[str]] = None) -> None:
    if env_args:
        envs = {i.split(":")[0]: i.split(":")[1] for i in env_args if len(i.split(":")) == 2}
        default_environ = dict(os.environ)
        e: Dict[str, str] = {}
        e.update(**default_environ)
        e.update(**envs)
        run_command(command, cwd=Path(cwd), env=e, visible=True, fail_exit=True)
    else:
        run_command(command, cwd=Path(cwd), visible=True, fail_exit=True)


__all__ = ["run_cmd"]
