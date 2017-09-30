import subprocess
import json
import shutil
from pathlib import Path


class InitRequirementMixin:
    """需要Install_mixin"""

    def _init_requirements(self, install=False)->int:
        """初始化依赖,但不会安装依赖"""
        print("copy requirements template")
        if self.form.compiler in ["python", "cython"]:
            dir_path = Path(__file__).parent.parent.parent.parent.joinpath(
                "source/requirements")
            local_path = Path(".")
            if local_path.joinpath("requirements").exists():
                print(str(local_path.joinpath("requirements")) + " exists")
            else:
                form_str = self.form.compiler + "_" + \
                    self.project_type + "_" + self.template + "_" + "requirements"
                if dir_path.joinpath(form_str).exists():
                    shutil.copytree(str(dir_path.joinpath(form_str)),
                                    str(local_path.joinpath("requirements")))
                else:
                    print('init ' + form_str + " not support now!")
                    return False

        elif self.form.compiler in ["node"]:
            print("node do not need to init requirements")
            return False

        elif self.form.compiler == "cpp":
            subprocess.call('conan install', shell=True)
        else:
            print("unkown compiler!")
            return False
        print("copy requirements template done!")
        return True


__all__ = ["InitRequirementMixin"]
