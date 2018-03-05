"""删除项目."""
import os
import stat
import shutil
from pathlib import Path


things = [""]


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


class CleanMixin:
    """删除项目混入."""

    def clean(self, total: bool=False):
        """删除目录下的内容.

        Args:

            total (bool, optional): 是否删除目录下的全部内容(Defaults to False).
        """
        path = Path(".").absolute()
        rms = ["document", "env", "dockerfile",
               "__pycache__", "test", "test_package",
               "CMakeFiles", "CMakeCache.txt"]
        for p in path.iterdir():
            if total is False:
                if p.name in rms:
                    if p.is_file():
                        try:
                            os.remove(str(p))
                        except Exception as e:
                            print(e)
                            print("skip " + str(path.joinpath(p)))
                            continue
                    else:
                        try:
                            shutil.rmtree(str(p), onerror=remove_readonly)
                        except Exception as e:
                            print(e)
                            print("skip " + str(path.joinpath(p)))
                            continue

                else:
                    continue
            else:
                if p.name.startswith("."):
                    continue
                else:
                    if p.is_file():
                        try:
                            os.remove(str(p))
                        except Exception as e:
                            print(e)
                            print("skip " + str(path.joinpath(p)))
                            continue
                    else:
                        try:
                            shutil.rmtree(str(p), onerror=remove_readonly)
                        except Exception as e:
                            print(e)
                            print("skip " + str(path.joinpath(p)))
                            continue
