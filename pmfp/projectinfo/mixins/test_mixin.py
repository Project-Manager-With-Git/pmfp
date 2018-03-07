"""测试代码用的模块"""
import subprocess
import unittest
from mypy import api
import coverage


class TestMixin:
    """需要PythonPathMixin."""

    def _run_python_test(self, html, g=False):
        print("unittest start")
        print("g")
        print(g)

        if g:
            # if self.form.project_form in ('sanic', 'flask'):
            #     cov = coverage.coverage(source=['{}/App'.format(self.meta.project_name)])
            #     suite = unittest.TestLoader().discover(".")
            # else:
            cov = coverage.coverage(source=['{}'.format(self.meta.project_name)])
            suite = unittest.TestLoader().discover(".")
            try:
                cov.start()
                unittest.TextTestRunner(verbosity=2).run(suite)
                cov.stop()
            except Exception as e:
                raise e
            else:
                if html:
                    cov.html_report(directory='covhtml')
                else:
                    cov.report()
        else:
            python_path = self._get_python_path()
            command = "{python_path} -m coverage run --source={package_name} -m unittest discover -v -s .".format(
                python_path=python_path,
                package_name=self.meta.project_name
            )
            try:
                print("test in {}".format(self.form.env))
                subprocess.check_call(command, shell=True)
            except Exception as e:
                print("error")
                raise e
            else:
                if html:
                    command = "{python_path} -m coverage html -d covhtml".format(
                        python_path=python_path)
                    subprocess.check_call(command, shell=True)
                else:
                    command = "{python_path} -m coverage report".format(
                        python_path=python_path)
                    subprocess.check_call(command, shell=True)

        print("unittest done!")

    def run_python_typecheck(self, html):
        """python类型检测."""
        print("type check start")
        if self.form.compiler == "python":
            if self.form.project_form == "script":
                package_name = self.meta.project_name + ".py"
            else:
                package_name = self.meta.project_name
            if html:
                result = api.run(
                    ["--ignore-missing-imports", '--html-report', 'typecheckhtml', package_name]
                )
            else:
                result = api.run(
                    ["--ignore-missing-imports", package_name]
                )
            if result[0]:
                print('\nType checking report:\n')
                print(result[0])  # stdout
            print("type check done!")
            return True
        else:
            print("only python can check type")
            return False

    def test(self, html=False, g=False):
        """测试项目,支持python和node."""
        if self.form.compiler == "python":
            self._run_python_test(html, g)
            return True
        # elif self.form.compiler == "cpp":
        #     command = "conan create demo/testing"
        #     subprocess.call(command, shell=True)
        #     return True
        elif self.form.compiler == "node":
            command = "npm run test"
            subprocess.call(command, shell=True)
            return True
        else:
            print("unknown compiler!")
            return False


__all__ = ["TestMixin"]
