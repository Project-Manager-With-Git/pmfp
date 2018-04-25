"""初始化环境"""
import sys
import json
import subprocess
import platform
from pathlib import Path


class InitEnvMixin:
    """初始化环境.

    需要InitDevRequirementMixin
    """

    def _init_env(self)->None:
        """初始化环境,只对python,js有用.

        初始化时会检测是否是python或者js项目,不是会抛出异常.
        接着会检测项目目录下是否有`env`文件夹,如果有的话会检测其是否和定义的一致,如果不一致则会抛出异常.
        然后会检测是否使用`global`环境,如果不是就会开始创建虚拟环境.如果环境未知也会抛出异常.

        Raises:
            AttributeError: 如果不是python项目,或者有env文件夹时env的定义与事实不符或者有未知的env时就会抛出异常

        """
        if self.form.compiler == "python":
            print("create dev requirement")
            self._init_dev_requirements()
            print("create dev requirement done!")
            path = Path("env")
            if path.exists():
                for i in path.iterdir():
                    if i.name in ("python", "python.exe"):
                        true_env = "conda"
                        break
                else:
                    true_env = "env"
                if true_env != self.form.env:
                    raise AttributeError(
                        "the exist env does not match with the project's setting")
                else:
                    print("already have a env")
                    return True
            if not self.form.env == "global":
                print('creating env')
                if self.form.env == "env":
                    if platform.system() == 'Windows':
                        python = "python"
                    else:
                        python = "python3"
                    command = [python, "-m", "venv", "env"]
                elif self.form.env == "conda":
                    command = ["conda", 'create', '-y', "-p", 'env', "python=" +
                               str(sys.version_info[0]) + "." + str(sys.version_info[1])]
                else:
                    raise AttributeError("unknown env")
                subprocess.check_call(command)
                print('creating env done!')
            

        elif self.form.compiler == "node":
            with open("package.json") as f:
                package = json.load(f)
            package.update(
                {
                    "name": self.meta.project_name,
                    "version": self.meta.version,
                    "description": self.desc.description,
                    "author": self.author.author + " <" + self.author.author_email + ">"
                }
            )
            with open("package.json", "w") as f:
                json.dump(package, f)
            return True
        else:
            raise AttributeError("{} do not need to set a env".format(self.form.compiler))


__all__ = ["InitEnvMixin"]
