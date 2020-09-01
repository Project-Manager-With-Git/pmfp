from pathlib import Path
from typing import Callable, Optional

def get_abs_path(path_str:str)->Path:
    """由路径字符串获取绝对路径.

    Args:
        path_str (str): 路径字符创

    Returns:
        Path: 路径字符串的绝对路径

    """
    rootp = Path(path_str)
    if rootp.is_absolute():
        root_path = rootp
    else:
        root_path = Path(".").absolute().joinpath(path_str)
    return root_path

def iter_dir_to_end(path:Path,
    match:Callable[[Path],bool],*,
    skip_dir:Optional[Callable[[Path],bool]]=None,
    succ_cb:Optional[Callable[[Path],None]]=None,
    fail_cb:Optional[Callable[[Path],None]]=None)->None:
    """遍历文件夹到底,并按指定的函数来做区分.

    Args:
        path (Path): 文件夹路径
        match (Callable[[Path],bool]): 筛选条件
        succ_cb (Optional[Callable[[Path],None]], optional): 路径满足筛选条件后执行的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[Path],None]], optional): 路径不满足筛选条件执行的回调函数. Defaults to None.

    """
    for p in path.iterdir():
        if p.is_dir():
            if skip_dir:
                if skip_dir(p):
                    continue
                else:
                    iter_dir_to_end(p,match,skip_dir=skip_dir,succ_cb=succ_cb,fail_cb=fail_cb)
            else:
                iter_dir_to_end(p,match,skip_dir=skip_dir,succ_cb=succ_cb,fail_cb=fail_cb)
        else:
            if match(p):
                if succ_cb:
                    succ_cb(p)
                else:
                    print(f"{p} matched")
            else:
                if fail_cb:
                    fail_cb(p)
                else:
                    print(f"{p} not match")
    