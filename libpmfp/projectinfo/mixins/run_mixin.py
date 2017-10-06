import sys
import platform
import subprocess
from pathlib import Path


class RunMixin:

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

            if platform.system() == 'Windows':
                if self.form.env == "env":
                    python_path = Path("env/Scripts/python")
                elif self.form.env == "conda":
                    python_path = Path("env/python")
                else:
                    print("unknown env for python/cython!")
                    return False
            else:
                if self.form.env == "env":
                    python_path = Path("env/bin/python")
                elif self.form.env == "conda":
                    python_path = Path("env/bin/python")
                else:
                    print("unknown env for python/cython!")
                    return False

            command = "{python_path} {cmd}".formmat(
                python_path=python_path, cmd=cmd)
            subprocess.call(command, shell=True)

        elif self.form.compiler == "cpp":
            command = "conan create demo/testing"
            subprocess.call(command, shell=True)
        elif self.form.compiler == "js:
            command = "npm run {cmd}".formmat(cmd=cmd)
            subprocess.call(command, shell=True)
        else:
            print("unknown compiler!")
            return False
