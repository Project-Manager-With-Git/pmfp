import sys
import subprocess
import platform
from pathlib import Path


class InitEnvMixin:
    def _init_env(self):
        """初始化虚拟环境,只对python,cython有用
        """
        if self.form.compiler not in ("python", "cython"):
            print(self.form.compiler, "do not need to set a env")
            return False
        path = Path("env")
        if path.exists():
            
            for i in path.iterdir():
                if i.name in ("python","python.exe"):
                    true_env = "conda"
                    break
            else:
                true_env = "env"
            if true_env != self.form.env:
                raise AttributeError("the exist env does not match with the project's setting")
            else:
                print("already have a env")
                return False

        print('creating env')
        if self.form.env == "env":
            if platform.system() == 'Windows':
                python = "python"
            else:
                python = "python3"
            command = [python, "-m", "venv", "env"]
        elif self.form.env == "conda":
            command = ["conda", 'create', "-p", 'env', "python=" +
                       str(sys.version_info[0]) + "." + str(sys.version_info[1])]
        else:
            print("unknown env")
            return False
        subprocess.check_call(command)
        print('creating env done!')
        return True


__all__ = ["InitEnvMixin"]
