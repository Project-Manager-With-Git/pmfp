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
    PMFP_CONFIG_PATH,
    PMFP_CONFIG_HOME,
    DEFAULT_PMFPRC,
    GOLBAL_PYTHON,
    GOLBAL_CC
)


def get_abs_path(path_str: str, root: Optional[Path] = None) -> Path:
    """由路径字符串获取绝对路径.

    Args:
        path_str (str): 路径字符创

    Returns:
        Path: 路径字符串的绝对路径

    """
    p = Path(path_str)
    if p.is_absolute():
        r_path = p
    else:
        if root:
            r_path = root.resolve().joinpath(path_str)
        else:
            r_path = Path(".").resolve().joinpath(path_str)
    return r_path


def iter_dir_to_end(path: Path,
                    match: Callable[[Path], bool], *,
                    skip_dir: Optional[Callable[[Path], bool]] = None,
                    succ_cb: Optional[Callable[[Path], None]] = None,
                    fail_cb: Optional[Callable[[Path], None]] = None) -> None:
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
                    iter_dir_to_end(p, match, skip_dir=skip_dir, succ_cb=succ_cb, fail_cb=fail_cb)
            else:
                iter_dir_to_end(p, match, skip_dir=skip_dir, succ_cb=succ_cb, fail_cb=fail_cb)
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


def init_pmfprc() -> None:
    """初始化pmfp的配置."""
    if not PMFP_CONFIG_PATH.exists():
        if not PMFP_CONFIG_HOME.exists():
            PMFP_CONFIG_HOME.mkdir(parents=True)
        config = {}
        config.update(DEFAULT_PMFPRC)
        with open(PMFP_CONFIG_PATH, "w") as fw:
            json.dump(config, fw, ensure_ascii=False, indent=4, sort_keys=True)


def get_cache_dir() -> Path:
    """获取缓存根目录."""
    init_pmfprc()
    with open(PMFP_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        cache_dir = Path(config["cache_dir"])
    return cache_dir


def get_global_python() -> str:
    """获取全局python."""
    init_pmfprc()
    with open(PMFP_CONFIG_PATH, "r") as f:
        pmfprc = json.load(f)
        return pmfprc.get("python", GOLBAL_PYTHON)


def get_global_cc() -> str:
    """获取全局c编译器."""
    init_pmfprc()
    with open(PMFP_CONFIG_PATH, "r") as f:
        pmfprc = json.load(f)
        return pmfprc.get("cc", GOLBAL_CC)
