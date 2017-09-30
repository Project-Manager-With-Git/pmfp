import platform
import subprocess
import shutil
from pathlib import Path
WINDOWS_ENV_BLACKLIST = ["mkl", 'numpy', 'scipy', 'scikit-learn']
WINDOWS_ENV_BLACKDICT = {
    "sanic": "set "
}
WINDOWS_CONDA_BLACKDICT = {
    "sanic": "set SANIC_NO_UVLOOP=true&set SANIC_NO_UJSON=true&{python_path} -m pip install git+https://github.com/channelcat/sanic.git"
}

PYTHON_REQUIREMENTS_PATH = {
    "requirement": "requirements/requirements.txt",
    "dev": "requirements/requirements_dev.txt",
    "test": "requirements/requirements_test.txt"
}


class InitRequirementMixin:

    def _install_node(self, line, record=False):
        pass

    def _install_python(self, line, record=False):
        if self.form.compiler not in ["python", "cython"]:
            print(self.form.compiler, "can not install with pip or conda")
            return False
        if platform.system() == 'Windows':
            if self.form.env == "env":
                python_path = Path("env\Scripts\python").absolute()
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
                if line in WINDOWS_ENV_BLACKDICT.keys():
                    command = WINDOWS_ENV_BLACKDICT[line]
                else:
                    command = "conda install -y {line}".format(line=line)
            else:
                print("unknown env!")
                return False
        else:
            if self.form.env == "env":
                python_path = Path("env/bin/python").absolute()
                command = "{python_path} -m pip install {line}".format(
                    python_path=python_path, line=line)
            elif self.form.env == "conda":
                command = "conda install -y -p env {}".format(line)
            else:
                print("unknown env!")
                return False
        try:
            subprocess.call(command, shell=True)
        except:
            raise
        else:
            print(line, "installed")
            if record:
                p = PYTHON_REQUIREMENTS_PATH.get(
                    record, "requirements/requirements.txt")
                with open(p) as f:
                    lines = f.read_lines()
                for i in lines:
                    if line == i.strip():
                        print(line, "already registed in ", p)
                        break
                else:
                    with open(p, "a") as f:
                        f.write(line + "\n")
            return True

    def _install_python_requirements(self, record="requirement"):
        print("install python requirement")
        p = PYTHON_REQUIREMENTS_PATH.get(
            record, "requirements/requirements.txt")
        with open(p) as f:
            lines = f.read_lines()
        for i in lines:
            line = i.strip()
            if line:
                try:
                    self._install_python(line)
                except Exception as e:
                    print(line, "install failed")
                    print(str(e))
                    continue
            else:
                continue
        return True



    def _init_makefile(self):
        raise NotImplementedError

    def _init_requirements(self)->int:
        print("copy requirements template")
        dir_path = Path(__file__).parent.parent.parent.parent.joinpath(
            "source/requirements")
        local_path = Path(".")
        if local_path.joinpath("requirements").exists():
            print(str(local_path.joinpath("requirements")) + " exists")
        else:
            form_str = self.form.compiler + "_" + \
                self.project_type + "_" + self.template + "_" + "requirements"
            if dir_path.joinpath(form_str).exists():
                if self.form.compiler in ["python","cython"]:
                    shutil.copytree(str(dir_path.joinpath(form_str)),
                                str(local_path.joinpath("requirements")))
                elif self.form.compiler in ["node"]:
                    if self.form.template == "vue":
                        subprocess.call('vue init webpack', shell=True)
                elif self.form.compiler == "cpp":
                    subprocess.call('conan install', shell=True)
                else:
                    print("unkown compiler!")


            else:
                print('init ' + form_str + " not support now!")
                return False
        print("copy requirements template done!")
        return 1


__all__ = ["InitRequirementMixin"]