import platform
import subprocess
import shutil
from pathlib import Path

WINDOWS_ENV_BLACKLIST = ["mkl", 'numpy', 'scipy', 'scikit-learn']
WINDOWS_ENV_BLACKDICT = {
    "sanic": "set SANIC_NO_UVLOOP=true&set SANIC_NO_UJSON=true&{python_path} -m pip install git+https://github.com/channelcat/sanic.git"
}
WINDOWS_CONDA_BLACKDICT = {
    "sanic": "set SANIC_NO_UVLOOP=true&set SANIC_NO_UJSON=true&{python_path} -m pip install git+https://github.com/channelcat/sanic.git",
    "flask-bootstrap": "{python_path} -m pip install flask-bootstrap",
    "boom": "{python_path} -m pip install boom"
}

PYTHON_REQUIREMENTS_PATH = {
    "requirement": "requirements/requirements.txt",
    "dev": "requirements/requirements_dev.txt"
}


class InstallMixin:
    def _install_node(self, line, record=False):
        """node 安装一条依赖."""
        if record == "requirement":
            command = "npm install {line} --save".format(line=line)
        elif record in ["dev", "test"]:
            command = "npm install {line} --save-dev".format(line=line)
        else:
            command = "npm install {line}".format(line=line)
        subprocess.call(command, shell=True)
        return True

    def _install_cpp(self, line, record=False):
        command = "conan install {line} -r conan-transit".format(line=line)
        subprocess.call(command, shell=True)
        return True

    def _install_python(self, line, record=False):
        """python 安装一条依赖.

        Args:

            line (line): - 依赖名
            record (str): - 指定安装在dev还是执行环境默认为False,意味不记录

        """
        if self.form.compiler != "python":
            print(self.form.compiler, "can not install with pip or conda")
            return False
        python_path = self._get_python_path()
        if platform.system() == 'Windows':
            if self.form.env == "env":
                if line in WINDOWS_ENV_BLACKLIST:
                    print("""windowsc an not install {line} through pip,
                    please go to http://www.lfd.uci.edu/~gohlke/pythonlibs and 
                    download the packages you need,then install""".format(line=line))
                    return False
                elif line in WINDOWS_ENV_BLACKDICT.keys():
                    command = WINDOWS_ENV_BLACKDICT[line].format(
                        python_path=python_path)
                else:
                    command = "{python_path} -m pip install {line}".format(
                        python_path=python_path, line=line)
            elif self.form.env == "conda":
                if line in WINDOWS_CONDA_BLACKDICT.keys():
                    command = WINDOWS_CONDA_BLACKDICT[line].format(
                        python_path=python_path)
                else:
                    command = "conda install -y {line} -p env".format(
                        line=line)
            else:
                command = "{python_path} -m pip install {line}".format(
                    python_path=python_path, line=line
                )
        else:
            if self.form.env == "env":
                python_path = Path("env/bin/python").absolute()
                command = "{python_path} -m pip install {line}".format(
                    python_path=python_path, line=line
                )
            elif self.form.env == "conda":
                command = "conda install -y -p env {}".format(line)
            else:
                command = "{python_path} -m pip install {line}".format(
                    python_path=python_path, line=line
                )
        try:
            print(command)
            subprocess.call(command, shell=True)
        except:
            raise
        else:
            print(line, "installed")
            if record:
                p = PYTHON_REQUIREMENTS_PATH.get(
                    record,
                    "requirements/requirements.txt"
                )
                with open(p) as f:
                    lines = f.readlines()
                for i in lines:
                    if line == i.strip():
                        print(line, "already registed in ", p)
                        break
                else:
                    with open(p, "a") as f:
                        f.write(line + "\n")
            return True

    def _install_python_requirements(self, record="requirement")->bool:
        """从依赖文件安装执行环境或者开发环境的依赖.

        Args:
            record (str, optional): 指定安装的依赖文件(Defaults to "requirement").

        Returns:
            (bool): 都安装正确返回True,否则False

        """
        print("install python requirement")
        if record != "all":
            p = PYTHON_REQUIREMENTS_PATH.get(
                record, "requirements/requirements.txt")
            with open(p) as f:
                lines = f.readlines()
        else:
            lines = []
            for _, v in PYTHON_REQUIREMENTS_PATH.items():
                if Path(v).exists():
                    with open(v) as f:
                        templines = f.readlines()
                        for i in templines:
                            lines.append(i)
        print("Will install {}".format(lines))
        error = False
        for i in lines:
            line = i.strip()
            if line:
                try:
                    self._install_python(line)
                except Exception as e:
                    print(line, "install failed")
                    print(str(e))
                    error = True
                    continue
            else:
                continue
        if error:
            return False
        return True

    def _install_node_requirements(self, record):
        if record == "requirement":
            command = "npm install --save"
        elif record in ["dev", "test"]:
            command = "npm install --save-dev"
        elif record == "all":
            command = "npm install"
        subprocess.call(command, shell=True)
        return True

    def _install_cpp_requirements(self, record):
        pass

    def install_requirements(self, record="requirement"):
        if self.form.compiler == "node":
            return self._install_node_requirements(record=record)
        elif self.form.compiler == "cpp":
            return self._install_cpp_requirements(record=record)
        elif self.form.compiler == "python":
            return self._install_python_requirements(record=record)
        else:
            print("unknown compiler!")
            return False

    def install(self, line, record="requirement"):
        if self.form.compiler == "node":
            return self._install_node(line, record=record)
        elif self.form.compiler == "cpp":
            return self._install_cpp(line, record=record)
        elif self.form.compiler == "python":
            return self._install_python(line, record=record)
        else:
            print("unknown compiler!")
            return False


__all__ = ["InstallMixin"]
