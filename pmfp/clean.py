"""清空项目."""
import os
import shutil
import stat
from typing import Callable, Any
from pmfp.const import PROJECT_HOME


def remove_readonly(func: Callable, path: str, _: Any)->None:
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _clean_total():
    """删除项目所有代码."""
    EXCEPT = ["pmfprc.json", ".git", ".gitignore"]
    for p in PROJECT_HOME.iterdir():
        if (p.name not in EXCEPT) and (not p.name.startswith(".")):
            if p.is_file():
                try:
                    os.remove(str(p))
                except Exception as e:
                    print(f"因为错误{str(e)}跳过删除文件 {str(p)}")
                    continue
            else:
                try:
                    shutil.rmtree(str(p), onerror=remove_readonly)
                except Exception as e:
                    print(f"因为错误{str(e)}跳过删除目录 {str(p)}")
                    continue
        else:
            continue


def _clean_rest():
    """删除项目的多余配置和代码."""
    rms = ["document", "env", "dockerfile", "node_modules",
           "__pycache__", "test", "test_package",
           "CMakeFiles", "CMakeCache.txt"]
    for p in PROJECT_HOME.iterdir():
        if p.name in rms:
            if p.is_file():
                try:
                    os.remove(str(p))
                except Exception as e:
                    print(f"因为错误{str(e)}跳过删除文件 {str(p)}")
                    continue
            else:
                try:
                    shutil.rmtree(str(p), onerror=remove_readonly)
                except Exception as e:
                    print(f"因为错误{str(e)}跳过删除目录 {str(p)}")
                    continue


def clean(total: bool = False):
    """清除多余的项目文件.

    Args:
        total (bool, optional): Defaults to False. 是否删除全部项目.
    """
    print("清理项目开始")
    if total:
        _clean_total()
    else:
        _clean_rest()
    print("清理项目结束")
