"""schema模块的公用工具."""
from typing import Optional
from pmfp.utils.template_utils import jsontemplate_2_content
from pmfp.utils.fs_utils import get_abs_path


def make_url_id(name: str, path: str, version_name: str, cwd: str, *,
                addr: Optional[str] = None) -> str:
    """构造json schema 的id.

    Args:
        name (str): 模式名
        path (str): 相对根路径的位置
        version_name (str): 模式版本
        cwd (str): 根路径
        addr (Optional[str], optional): 有addr则表明url为http的url,否则使用file url来定义id. Defaults to None.

    Returns:
        str: [description]

    """
    root_path = get_abs_path(cwd)
    if addr:
        _id = f"http://{addr}/{path}/{name}/{version_name}/{name}.schema.json"
    else:
        file_path = root_path.joinpath(path).joinpath(f"{name}/{version_name}/{name}.schema.json")
        _id = file_path.as_uri()
    return _id


def copy_schema(template: str, name: str, path: str, version_name: str, cwd: str, *,
                addr: Optional[str] = None) -> None:
    """以一个json schema 为模板copy一个json schema文件.

    Args:
        name (str): 模式名
        path (str): 从根目录起的路径
        version_name (str): 模式版本,形式为`v0_0_0`
        cwd (str): 根目录.
        addr (str, optional): 网站域名.

    """
    _id = make_url_id(name=name, path=path, version_name=version_name, cwd=cwd, addr=addr)
    root_path = get_abs_path(cwd)
    filepath = root_path.joinpath(f"{path}/{name}/{version_name}/{name}.schema.json")
    parentpath = filepath.parent
    kwargs = {
        "$id": _id
    }
    content = jsontemplate_2_content(template=template, **kwargs)
    if parentpath.exists():
        if parentpath.is_file():
            raise AttributeError(f"{parentpath} is file")
    else:
        parentpath.mkdir(parents=True)
    with open(str(filepath), "w", newline="", encoding="utf-8") as f:
        f.write(content)
