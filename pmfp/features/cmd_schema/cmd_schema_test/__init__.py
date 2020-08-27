"""检测json schema的example是否符合定义的模式schema."""
import json
from pathlib import Path
from typing import NoReturn,Optional
from utils.url_utils import is_http_url,is_file_url,is_url




def test_schema(file:str) -> NoReturn:
    """检查一个json schema文件中的例子是否符合自身的schema.

    Args:
        file (str): 模式文件地址

    """
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
