"""创建json schema的schema."""
import warnings
import pkgutil
import subprocess
import json
from pathlib import Path
from typing import NoReturn,Optional
import chardet
from pmfp.utils.template_utils import jsontemplate_2_content

schema_template = pkgutil.get_data('pmfp.features.cmd_schema.cmd_schema_new.schematemp', 'schema.json').decode('utf-8')




def new_schema(name:str,path:str,version:str,root:str,addr:Optional[str]=None) -> NoReturn:
    """新建一个json schema文件.

    Args:
        name (str): 模式名
        path (str): 从根目录起的路径
        version (str): 模式版本
        root (str): 根目录.
        addr (str, optional): 网站域名.

    """
    version_name = "_".join(version.split("."))
    root = Path(root)
    if root.is_absolute():
        root_path = root
    else:
        root_path = Path(".").absolute().joinpath(root)

    if addr:
        _id = f"http://{addr}/{path}/{name}/{version_name}/{name}.schema.json"
    else:
        dir_path = root_path.joinpath(path)
        dir_str = str(dir_path)
        _id = f"file:///{dir_str}/{name}/{version_name}/{name}.schema.json"

    filepath = root_path.joinpath(f"{path}/{name}/{version_name}/{name}.schema.json")
    parentpath = filepath.parent
    kwargs = {
        "$id": _id
    }
    content = jsontemplate_2_content(template=schema_template,**kwargs)
    if parentpath.exists():
        if parentpath.is_file():
            raise AttributeError(f"{parentpath} is file")
    else:
        parentpath.mkdir(parents=True)
    with open(str(filepath),"w") as f:
        f.write(content)
