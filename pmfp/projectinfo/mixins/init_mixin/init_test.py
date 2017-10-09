import shutil
from string import Template
from pathlib import Path

PYTHON_WEB_TEST = Template("""import sys
from pathlib import Path
file_path = Path(__file__)
target_pyz_path = file_path.parent.parent.joinpath("$project_name.pyz")
target_project_path = file_path.parent.parent.joinpath("$project_name")
if target_pyz_path.exists():
    target = str(target_pyz_path)
else:
    target = str(target_project_path)
sys.path.insert(0, target)

from app_creater import create_app
from config import choose_conf

app = create_app(choose_conf("testing"))

""")


class InitTestMixin:
    """需要InstallMixin,Temp2pyMixin
    """

    def _init_test_python_web(self):
        if self.form.compiler in ["python", "cython"]:
            if self.form.project_type == "web":
                if self.form.template not in ["flask", "sanic"]:
                    with open("test/get_app.py", "w") as f:
                        content = PYTHON_WEB_TEST.substitute(
                            project_name=self.meta.project_name)
                        f.write(content)
                    return True
        return False

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
                    self.form.project_type + "_" + self.form.template + "_" + "test"
                if dir_path.joinpath(form_str).exists():
                    shutil.copytree(str(dir_path.joinpath(form_str)),
                                    str(local_path.joinpath("test")))
                else:
                    print('init ' + form_str + " not support now!")
                    return False
            self.temp2py(local_path.joinpath('test'))
            print("copy test template done!")
            print("write get_app.py in test")
            self._init_test_python_web()
            print("write get_app.py in test done")
            if install:
                self._install_python_requirements(record="test")
                print("#################################################")
                print("test installed")
                print("#################################################")
            return True
        elif self.form.compiler == "node":
            # todo node的测试先放着
            return True
        else:
            print("unknown compiler to init test")
            return False

    __all__ = ["InitTestMixin"]
