import shutil
from pathlib import Path


class InitTestMixin:
    """需要InstallMixin
    """
    def _init_test(self, install=False):
        """初始化测试
        """
        if self.form.compiler == "cpp":
            # cpp的测试在模板初始化那一步做
            return True

        elif self.form.compiler in ["python", 'cython']:
            print("copy test template")
            dir_path = Path(__file__).parent.parent.parent.parent.joinpath(
                "source/tests")
            local_path = Path(".")
            if local_path.joinpath("test").exists():
                print(str(local_path.joinpath("test")) + " exists")
                return False
            else:
                form_str = self.form.compiler + "_" + \
                    self.project_type + "_" + self.template + "_" + "test"
                if dir_path.joinpath(form_str).exists():
                    shutil.copytree(str(dir_path.joinpath(form_str)),
                                    str(local_path.joinpath("test")))
                else:
                    print('init ' + form_str + " not support now!")
                    return False
            print("copy test template done!")
            return True
        elif self.form.compiler == "node":
            # todo node的测试先放着
            return True
        else:
            print("unknown compiler to init test")
            return False

    __all__ = ["InitTestMixin"]
