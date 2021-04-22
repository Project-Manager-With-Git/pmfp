"""创建json schema的schema."""
import pkgutil
import json
from pathlib import Path
from typing import Optional

from ..utils import copy_schema
from .core import schema_new

schema_template = ""
schema_template_io = pkgutil.get_data('pmfp.entrypoint.schema.new.source_temp', 'schema.json.jinja')
if schema_template_io:
    schema_template = schema_template_io.decode('utf-8')
else:
    raise AttributeError("加载json schema 模板失败")


@schema_new.as_main
def new_schema(name: str, to: str, version: str, *, cwd: str = ".", addr: Optional[str] = None) -> None:
    """新建一个json schema文件.

    Args:
        name (str): 模式名
        to (str): 目标路径
        version (str): 模式版本
        cwd (str): 执行目录.
        addr (Optional[str]): 网站域名.

    """
    version_name = "_".join(version.split("."))
    copy_schema(template=schema_template, name=name, path=to, version_name=version_name, cwd=cwd, addr=addr)
