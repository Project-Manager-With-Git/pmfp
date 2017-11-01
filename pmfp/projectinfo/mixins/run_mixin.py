import subprocess
from pathlib import Path


class RunMixin:
    """需要PythonPathMixin
    """

    def run(self, cmd=""):
        if self.form.compiler in ["cython", "python"]:
            if cmd == "":
                if Path(self.meta.project_name + ".py").exists():
                    cmd = self.meta.project_name + ".py"
                if Path(self.meta.project_name + ".pyz").exists():
                    cmd = self.meta.project_name + ".pyz"
            if cmd == "":
                print("need a cmd")
                raise AttributeError("need a cmd")

            python_path = self._get_python_path()
            if python_path:
                command = "{python_path} {cmd}".format(
                    python_path=python_path, cmd=cmd)
                subprocess.call(command, shell=True)
            else:
                print("no python path")
                return False

        elif self.form.compiler == "cpp":
            command = "conan create demo/testing"
            subprocess.call(command, shell=True)
        elif self.form.compiler == "node":
            # 注意要先将es6或者typescript 编译为node可运行的代码
            if cmd == "":
                command = "npm run"
            else:
                command = "node --use_strict {cmd}".formmat(cmd=cmd)
            subprocess.call(command, shell=True)
        else:
            print("unknown compiler!")
            return False


__all__ = ["RunMixin"]
