"""文件系统相关的通用组件."""
import json
import os
import stat
import shutil
import tempfile
from pathlib import Path
from typing import (
    Callable,
    Optional,
    Any
)
from pmfp.const import (
    PLATFORM
)


def get_abs_path(path_str: str, cwd: Optional[Path] = None) -> Path:
    """由路径字符串获取绝对路径.

    Args:
        path_str (str): 路径字符创
        cwd (Optional[Path]): 指定执行时的位置

    Returns:
        Path: 路径字符串的绝对路径

    """
    p = Path(path_str)
    if p.is_absolute():
        r_path = p
    else:
        if cwd:
            r_path = cwd.resolve().joinpath(path_str)
        else:
            r_path = Path(".").resolve().joinpath(path_str)
    return r_path


def path_to_str(p: Path) -> str:
    if PLATFORM == 'Windows':
        source_dirp_str = str(p).replace("\\", "\\\\")
    else:
        source_dirp_str = str(p)
    return source_dirp_str


def get_abs_path_str(path_str: str, cwd: Optional[Path] = None) -> str:
    """由路径字符串获取绝对路径.

    Args:
        path_str (str): 路径字符创
        cwd (Optional[Path]): 指定执行时的位置

    Returns:
        str: 路径字符串的绝对路径字符串

    """
    source_dirp = get_abs_path(path_str, cwd)
    return path_to_str(source_dirp)


def iter_dir_to_end(path: Path,
                    match: Callable[[Path], bool], *,
                    skip_dir: Optional[Callable[[Path], bool]] = None,
                    succ_cb: Optional[Callable[[Path], None]] = None,
                    fail_cb: Optional[Callable[[Path], None]] = None,
                    skip_dir_handdler: Optional[Callable[[Path], None]] = None
                    ) -> None:
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
                    if skip_dir_handdler:
                        skip_dir_handdler(p)
                    else:
                        print(f"{p} skiped")
                else:
                    iter_dir_to_end(p, match, skip_dir=skip_dir, succ_cb=succ_cb, fail_cb=fail_cb, skip_dir_handdler=skip_dir_handdler)
            else:
                iter_dir_to_end(p, match, skip_dir=skip_dir, succ_cb=succ_cb, fail_cb=fail_cb, skip_dir_handdler=skip_dir_handdler)
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


def remove_readonly(func: Callable, path: str, _: Any) -> None:
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def tempdir(p: Path, cb: Callable[[Path], None]) -> None:
    """临时文件夹相关处理.

    Args:
        p (Path): 临时文件夹所在的文件夹
        cb (Callable[[Path],None]): 创建临时文件夹后的操作.

    """
    print("构造临时文件夹ing...")
    temp_dir = tempfile.TemporaryDirectory(suffix="pmfp_cache", dir=p)
    temp_path = p.joinpath(temp_dir.name)
    cb(temp_path)
    try:
        temp_dir.cleanup()
    except PermissionError:
        try:
            shutil.rmtree(str(temp_path), onerror=remove_readonly)
        except Exception as e:
            print(f"因为错误{str(e)}跳过删除目录 {str(p)}")
    except Exception as e:
        raise e


def delete_source(root_path: Path, *,
                  file_predication: Optional[Callable[[Path], bool]] = None,
                  dir_predication: Optional[Callable[[Path], bool]] = None,
                  dir_iter_filter: Optional[Callable[[Path], bool]] = None) -> None:
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

    def remove_readonly(func: Callable[[Path], None], path: Path, _: Any) -> None:
        """Clear the readonly bit and reattempt the removal."""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def _delete_source(p: Path) -> None:
        """递归的删除根目录下需要删除的文件.
        Args:
            p (Path): 要判断时候要删除的路径
        """
        if p.is_file():
            if file_predication and file_predication(p):
                os.remove(p)
        else:
            if dir_predication and dir_predication(p):
                try:
                    shutil.rmtree(p, onerror=remove_readonly)
                except Exception as e:
                    print(e)
            for child_path in filter(dir_iter_filter, p.iterdir()):
                _delete_source(child_path)

    if any([callable(file_predication), callable(dir_predication)]):
        _delete_source(root_path)
    else:
        raise AttributeError("file_predication和dir_predication必须至少有一个.")
