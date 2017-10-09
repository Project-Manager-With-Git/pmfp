import subprocess


class TestMixin:
    """需要PythonPathMixin"""

    def _run_python_test(self, html):
        print("unittest start")
        python_path = self._get_python_path()
        command = "{python_path} -m coverage run --source={package_name} -m unittest discover -v -s test".format(
            python_path=python_path,
            package_name=self.meta.project_name)
        try:
            subprocess.check_call(command)
        except Exception as e:
            print("error")
        else:
            command = "{python_path} -m coverage report".format(
                python_path=python_path)
            subprocess.check_call(command)
            if html:
                command = "{python_path} -m coverage html -d covhtml".format(
                    python_path=python_path)
                subprocess.check_call(command)
            self._run_python_typecheck(html=html)
        print("unittest done!")
        return True

    def _run_python_typecheck(self, html, package=None):
        print("type check start")
        if self.form.compiler in ["python", "cython"]:
            python_path = self._get_python_path()
            if self.form.project_type in ["command", "script", "model"]:
                if package is None:
                    package_name = self.meta.project_name
                    if self.form.project_type == "script":
                        package_name = package_name + ".py"
                else:
                    package_name = package
                if html:
                    command = "{python_path} -m mypy --ignore-missing-imports --html-report typecheckhtml {package_name}".format(
                        python_path=python_path,
                        package_name=package_name)
                else:
                    command = "{python_path} -m mypy {package_name}".format(
                        python_path=python_path,
                        package_name=package_name)

                try:
                    subprocess.check_call(command)
                except Exception as e:
                    print("error")
            else:
                # command = "{python_path} -m mypy --ignore-missing-imports --html-report typecheck {package_name}/App".format(
                #     python_path=python_path,
                #     package_name=package_name)
                # subprocess.check_call(command)
                print("type check not support the project type now")
            print("type check done!")
            return True
        else:
            print("only python can check type")
            return False

    def test(self, html=False):
        if self.with_test:
            if self.form.compiler in ["cython", "python"]:
                self._run_python_test(html)
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
