"""创建json schema的schema."""
import os
import json
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional,Dict
from pmfp.utils.template_utils import jsontemplate_2_content
from pmfp.utils.url_utils import is_file_url,is_http_url
from pmfp.utils.fs_utils import iter_dir_to_end,get_abs_path
from pmfp.features.cmd_schema.utils import copy_schema,make_url_id


def parse_id_from_relative_path(relative_path:Path)->Dict[str,str]:
    """从相对路劲来解析id中的构造参数.

    Args:
        relative_path (Path): 相对路径

    Returns:
        Dict[str,str]: 构造id时的参数字段

    """
    file_name= relative_path.name
    version_str = relative_path.parent.name
    schema_name = relative_path.parent.parent.name
    schema_path = relative_path.parent.parent.parent.as_posix()
    return {
        "name":schema_name,
        "version_name":version_str,
        "path":schema_path
    }

def parse_id(url:str,root:str)->Dict[str,str]:
    """从url中提取文件系统中的路径.

    Args:
        url (str): file url

    Returns:
        str: file url中提取出的路径

    """
    root_path = get_abs_path(root)
    if is_file_url(url):
        path_str = urlparse(url).path
        if ":" in path_str:
            path = path_str[1:]
        else:
            path = path_str

        file_path = Path(path)
        relative_path = file_path.relative_to(root_path)
        params = parse_id_from_relative_path(relative_path)
        params.update({
            "root":root_path.as_posix()
        })
        return params
    elif is_http_url(url):
        path_str = urlparse(url).path[1:]
        print(path_str)
        relative_path = Path(path_str)
        params = parse_id_from_relative_path(relative_path)
        params.update({
            "root":root_path.as_posix()
        })
        return params
    else:
        raise AttributeError(f"未知的url类型{url}")

def _move_schema(schema_file:str,old_root:str,*,
        new_name:Optional[str]=None,
        new_path:Optional[str]=None,
        new_version:Optional[str]=None,
        new_root:Optional[str]=None,
        new_addr:Optional[str]=None,
        remove_old:bool=False)->None:
    with open(schema_file, "r", encoding="utf-8") as f:
        old_schema_str = f.read()
    old_schema = json.loads(old_schema_str)
    old_schema_id = old_schema.get("$id")
    root_path = get_abs_path(old_root)
    params = {"root":root_path.as_posix()}
    old_params = parse_id(old_schema_id,old_root)
    params.update(old_params)
    if new_name is not None:
        params["name"]=new_name
    if new_path is not None:
        params["path"]=new_path
    if new_version is not None:
        params["version_name"]="_".join(new_version.split("."))
    if new_root is not None:
        new_root_path = get_abs_path(new_root)
        params["root"]=new_root_path.as_posix()
    if new_addr is not None:
        params["addr"]=new_addr
    if old_params["name"]==params["name"] and old_params["path"]==params["path"] and old_params["version_name"]==params["version_name"] and old_params["root"]==params["root"]:
        _id = make_url_id(**params)
        old_schema.update({"$id":_id})
        with open(schema_file, "w") as f:
            json.dump(old_schema,f,ensure_ascii=False,indent=4,sort_keys=True)
    else:
        copy_schema(old_schema_str,**params)
        if remove_old is True:
            try:
                os.remove(schema_file)
            except Exception as e:
                print(f"因为错误{str(e)}跳过删除文件 {str(old_schema_str)}")
    



def move_schema(file:str,old_root:str,*,
        name:Optional[str]=None,
        path:Optional[str]=None,
        version:Optional[str]=None,
        root:Optional[str]=None,
        addr:Optional[str]=None,
        remove_old:bool=False) -> None:
    """新建一个json schema文件.

    Args:
        name (str): 模式名
        path (str): 从根目录起的路径
        version (str): 模式版本
        root (str): 根目录.
        addr (str, optional): 网站域名.

    """
    file_path = Path(file)
    if file_path.is_dir():
        iter_dir_to_end(
            file_path,
            lambda p: p.is_file() and ".schema.json" in p.name,
            succ_cb= lambda p: _move_schema(
                schema_file=p.as_posix(),
                old_root=old_root,
                new_name=name,
                new_path=path,
                new_version=version,
                new_root=root,
                new_addr=addr,
                remove_old=remove_old
            )
        )
    elif file_path.is_file() and ".schema.json" in file_path.name:
        _move_schema(
            schema_file=file,
            old_root=old_root,
            new_name=name,
            new_path=path,
            new_version=version,
            new_root=root,
            new_addr=addr,
            remove_old=remove_old
        )
    else:
        print(f"路径{file}不是文件夹也不是以`.schema.json`结尾的模式定义文件")