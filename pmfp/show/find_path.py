"""用于遍历文件系统以找到需要的路径.

使用方法:
>>> from pathlib import Path
>>> pp = Path('.')
>>> ps = find_component(p1,lambda path,maxdepth: maxdepth == 2,2)
"""
from pathlib import Path
from typing import (
    List,
    Any,
    Callable,
    Optional
)


def find_path(path: Path, func: Callable[[Path, Optional[int]], bool], max_depth: Optional[int]=None, find_hide: bool=False)->List[Path]:
    """找到符合条件的地址对象.

    Args:
        path (Path): 要查找的根目录
        func (Callable[[Path, Optional[int]], bool]): 满足该函数的值为True,则将路径填入result,函数的参数为[Path对象,从0开始计数的当前深度]
        max_depth (Optional[int], optional): Defaults to None. 最大深度,允许为None,意为迭代到最大深度
        find_hide (bool, optional): Defaults to False. 是否连隐藏文件/文件夹也查找

    Returns:
        List[Path]: 符合条件的Path对象列表
    """

    def _find_iter(parent_path: Path, result: List[Any], func: Callable[[Path, Optional[int]], bool], maxdepth: Optional[int]=None, find_hide: bool=False):
        """查找路径下是否有满足条件路径的迭代.

        Args:
            parent_path (Path): 要查找的父路径
            result (List[Any]): 保存找到路径的容器
            func (Callable[[Path, Optional[int]], bool]): 满足该函数的值为True,则将路径填入result,函数的参数为[Path对象,从0开始计数的当前深度]
            maxdepth (Optional[int], optional): Defaults to None. 最大深度,允许为None,意为迭代到最大深度
            find_hide (bool, optional): Defaults to False. 是否连隐藏文件/文件夹也查找
        """
        if maxdepth is not None:
            if maxdepth == -1:
                return
        for path in parent_path.iterdir():
            if find_hide is False and path.name.startswith("."):
                continue
            if max_depth is None:
                depth = None
            else:
                depth = max_depth - maxdepth
            if func(path, depth):
                result.append(path)
            if path.is_dir():
                if maxdepth is None:
                    _find_iter(path, result, func)
                else:
                    next_maxdepth = maxdepth - 1
                    _find_iter(path, result, func, next_maxdepth)
    result = []
    _find_iter(path, result, func, maxdepth=max_depth, find_hide=find_hide)
    return result
