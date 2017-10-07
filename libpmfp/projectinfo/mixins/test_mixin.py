import subprocess


class TestMixin:
    """需要PythonPathMixin"""

    def _run_python_test(self):
        print("unittest start")
        python_path = self._get_python_path()
        command = "{python_path} -m coverage run --source={package_name} -m unittest discover -v -s test".format(
            python_path=python_path,
            package_name=self.meta.project_name)
        subprocess.check_call(command)
        print("unittest done!")
        return True

    def _run_python_typecheck(self):
        print("type check start")
        python_path = self._get_python_path()
        if self.form.project_type in ["command", "script", "model"]:
            package_name = self.meta.project_name
            if form == "script":
                package_name = package_name + ".py"
            command = "{python_path} -m mypy --ignore-missing-imports --html-report typecheck {package_name}".format(
                python_path=python_path,
                package_name=package_name)
            subprocess.check_call(command)

        else:
            command = "{python_path} -m mypy --ignore-missing-imports --html-report typecheck {package_name}/App".format(
                python_path=python_path,
                package_name=package_name)
            subprocess.check_call(command)
        print("type check done!")
        return True

    def test(self, typecheck=False):
        if self.with_test:
            if self.form.compiler in ["cython", "python"]:
                if typecheck:
                    self._run_python_typecheck()
                self._run_python_test()
                return True

            elif self.form.compiler == "cpp":
                command = "conan create demo/testing"
                subprocess.call(command, shell=True)
                return True
            elif self.form.compiler == "node":
                command = "npm run test"
                subprocess.call(command, shell=True)
                return True
            else:
                print("unknown compiler!")
                return False
        else:
            print('this project do not have test')


__all__ = ["TestMixin"]
