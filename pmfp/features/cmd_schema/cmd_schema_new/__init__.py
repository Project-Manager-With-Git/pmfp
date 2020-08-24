"""创建protobuf的schema."""
import subprocess
import warnings
from pathlib import Path
import pkgutil
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
    root = Path(root)
    if root.is_absolute():
        root_path = root
    else:
        root_path = Path(".").absolute().joinpath(root)

    if addr:
        _id = f"http://{addr}/{path}/{name}/{version}.json"
    else:
        dir_path = root_path.joinpath(path)
        dir_str = str(dir_path)
        _id = f"file:///{dir_str}/{name}/{version}.json"

    
    kwargs = {
        "$id": _id
    }
    content = jsontemplate_2_content(template=schema_template,**kwargs)

    
    
