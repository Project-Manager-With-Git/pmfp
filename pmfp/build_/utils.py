"""build_下的通用工具."""
import os
import stat
import shutil
from pathlib import Path
from typing import Callable, Any, Optional


def delete_source(
        root_path: Path, *,
        file_predication: Optional[Callable] = None,
        dir_predication: Optional[Callable] = None,
        dir_iter_filter: Optional[Callable] = None)->None:
    """删除源文件.

    file_predication和dir_predication必须至少有一个.

    Args:
        root_path (Path): [description]
        file_predication (Optional[Callable]): 用于判断文件是否要被删除的谓词,参数为p:path
        dir_predication (Optional[Callable]): 用于判断文件夹是否要被删除的谓词,参数为p:path
        dir_iter_filter (Optional[Callable]): 用于过夏季目录中不用迭代的部分
    """
    if not callable(file_predication):
        file_predication = None
    if not callable(dir_predication):
        dir_predication = None
    if not callable(dir_iter_filter):
        dir_iter_filter = None

    def remove_readonly(func: Callable, path: Path, _: Any)->None:
        """Clear the readonly bit and reattempt the removal."""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def _delete_source(p: Path):
        """递归的删除根目录下需要删除的文件.

        Args:
            p (Path): 要判断时候要删除的路径
        """
        if p.is_file():
            if file_predication and file_predication(p):
                os.remove(str(p))
        else:
            if dir_predication and dir_predication(p):
                try:
                    shutil.rmtree(str(p), onerror=remove_readonly)
                except Exception as e:
                    print(e)
            for child_path in filter(dir_iter_filter, p.iterdir()):
                _delete_source(child_path)

    if any([callable(file_predication), callable(dir_predication)]):
        _delete_source(root_path)
    else:
        raise AttributeError("file_predication和dir_predication必须至少有一个.")
