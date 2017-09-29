import shutil
from pathlib import Path


class InitTestMixin:

    def _init_test(self):
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

    __all__ = ["InitTestMixin"]
