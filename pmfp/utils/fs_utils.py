from pathlib import Path
from typing import Callable,NoReturn,Optional

def iter_dir_to_end(path:Path,
    match:Callable[[Path],bool],*,
    skip_dir:Optional[Callable[[Path],bool]]=None,
    succ_cb:Optional[Callable[[Path],NoReturn]]=None,
    fail_cb:Optional[Callable[[Path],NoReturn]]=None)->NoReturn:
    """遍历文件夹到底,并按指定的函数来做区分.

    Args:
        path (Path): 文件夹路径
        match (Callable[[Path],bool]): 筛选条件
        succ_cb (Optional[Callable[[Path],NoReturn]], optional): 路径满足筛选条件后执行的回调函数. Defaults to None.
        fail_cb (Optional[Callable[[Path],NoReturn]], optional): 路径不满足筛选条件执行的回调函数. Defaults to None.

    """
    for p in path.iterdir():
        if p.is_dir():
            if skip_dir:
                if skip_dir(p):
                    continue
                else:
                    iter_dir_to_end(p)
            else:
                iter_dir_to_end(p)
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
    