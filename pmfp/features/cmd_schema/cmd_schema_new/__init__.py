"""创建json schema的schema."""
import pkgutil
import json
from pathlib import Path
from typing import Optional

from pmfp.features.cmd_schema.utils import copy_schema

schema_template = ""
schema_template_io = pkgutil.get_data('pmfp.features.cmd_schema.cmd_schema_new.schematemp', 'schema.json')
if schema_template_io:
    schema_template = schema_template_io.decode('utf-8')
else:
    raise AttributeError("加载json schema 模板失败")


def new_schema(name:str,path:str,version:str,root:str,addr:Optional[str]=None) -> None:
    """新建一个json schema文件.

    Args:
        name (str): 模式名
        path (str): 从根目录起的路径
        version (str): 模式版本
        root (str): 根目录.
        addr (str, optional): 网站域名.

    """
    
    version_name = "_".join(version.split("."))
    copy_schema(template= schema_template,name=name,path=path,version_name=version_name,root=root,addr=addr)