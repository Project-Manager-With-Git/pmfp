import shutil
import subprocess
from pathlib import Path


class BuildMixin:
    def build(self, egg=False, wheel=False):
        if self.form.compiler == "python":
            if self.form.project_type in ["gui"] and self.form.template not in ["tk"]:
                print('build self.meta.peoject_name to pyz file'.format(self=self))
                command = 'python -m zipapp {self.meta.peoject_name} -m "main:main" -p "/usr/bin/env python3"'.format(
                    self=self)
                subprocess.call(command, shell=True)
                print('build self.meta.peoject_name to pyz file done!'.format(self=self))
                return True
            elif self.form.project_type in ["web"] and self.form.template not in ["flask", "sanic"]:
                print('move template and static files')
                here = Path(".").absolute()
                name = self.meta.project_name
                static = here.joinpath(name).joinpath("static")
                templates = here.joinpath(name).joinpath("templates")
                dir_static = here.joinpath("static")
                dir_templates = here.joinpath("templates")
                if static.exists():
                    shutil.copytree(str(static),
                                    str(dir_static))
                    print("move static files done!")
                    shutil.rmtree(str(static))
                    print("remove original static files done!")
                if templates.exists():
                    shutil.copytree(str(templates),
                                    str(dir_templates))
                    print("move template files done!")
                    shutil.rmtree(str(templates))
                    print("remove original templates files done!")

                print('move template and static files done!')
                print('build {self.meta.project_name} to pyz file'.format(self=self))
                command = 'python -m zipapp {self.meta.project_name} -m "main:main" -p "/usr/bin/env python3"'.format(
                    self=self)
                subprocess.call(command, shell=True)
                print('build {self.meta.project_name} to pyz file done!'.format(self=self))
                return True

            elif self.form.project_type in ["command", "celery", "model"]:
                if egg:
                    print('build model to egg file')
                    command = "python setup.py bdist_egg"
                    subprocess.check_call(command)
                    print('build model to egg file done!')

                if wheel or not any([egg, wheel]):
                    print('build model to wheel file')
                    command = "python setup.py bdist_wheel"
                    subprocess.check_call(command)
                    print('build model to wheel file done!')
                return True

            elif self.form.project_type in ["script"]:
                print("script do not need to build")
                return False

            else:
                print("unkown form")
                return False
        elif self.form.compiler == "cython":
            print('build cython model')
            command = 'python setup.py build_ext --inplace'
            subprocess.check_call(command)
            print('build cython model done!')
            if self.form.project_type in ["script"]:
                print("script do not need to build")
                return False
            elif self.form.project_type in ["model", "command", "celery"]:
                if egg:
                    print('build model to egg file')
                    command = "python setup.py bdist_egg"
                    subprocess.check_call(command)
                    print('build model to egg file done!')

                if wheel or not any([egg, wheel]):
                    print('build model to wheel file')
                    command = "python setup.py bdist_wheel"
                    subprocess.check_call(command)
                    print('build model to wheel file done!')
                return True
            else:
                print("unkown form")
                return False

        elif self.form.compiler == "cpp":
            command = "conan build"
            subprocess.call(command, shell=True)
            return True
        elif self.form.compiler == "node":
            # 注意要先将es6或者typescript 编译为node可运行的代码

            command = "npm run build"
            subprocess.call(command, shell=True)
        else:
            print("unknown compiler!")
            return False


__all__ = ["BuildMixin"]
