import os
import stat
import shutil
from pathlib import Path


things = [""]


def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)


class CleanMixin:

    def clean(self, all=False):
        path = Path(".").absolute()
        rms = ["document", "env", "dockerfile",
               "__pycache__", "test", "test_package",
               "CMakeFiles", "CMakeCache.txt"]
        for p in path.iterdir():
            if all is False:
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
        else:
            return True
