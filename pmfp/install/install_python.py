import json
import subprocess
from typing import (
    Dict,
    Any,
    Optional
)
from pmfp.const import PLATFORM, PMFPRC_PATH
from pmfp.utils import get_python_path

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


def install(config: Dict[str, Any], package: Optional[str]=None, dev: bool=False):
    """python 安装一条依赖.

    Args:
        config (Dict[str,Any]): 现有配置
        package (Optional[str]): 依赖名,默认为None,意为安装配置中的依赖
        dev (bool): 指定安装在dev还是执行环境,默认为False

    """
    python_path = get_python_path(config)
    if package is None:
        if dev is True:
            requirement = config["requirement-dev"]
        else:
            requirement = config["requirement"]
        for package in requirement:
            if PLATFORM == 'Windows':
                if config["env"] == "conda":
                    if package in WINDOWS_CONDA_BLACKDICT.keys():
                        command = WINDOWS_CONDA_BLACKDICT[package].format(
                            python_path=python_path)
                    else:
                        command = f"conda install -y {package} -p env"
                elif config["env"] == "env":
                    if package in WINDOWS_ENV_BLACKLIST:
                        print(f"""windowsc an not install {package} through pip,
                        please go to http://www.lfd.uci.edu/~gohlke/pythonlibs and 
                        download the packages you need,then install""")
                        return False
                    elif package in WINDOWS_ENV_BLACKDICT.keys():
                        command = WINDOWS_ENV_BLACKDICT[package].format(python_path=python_path)
                    else:
                        command = f"{python_path} -m pip install {package}"
            else:
                if config["env"] == "env":
                    command = f"{python_path} -m pip install {package}"
                elif config["env"] == "conda":
                    command = f"conda install -y -p env {package}"
            try:
                subprocess.check_call(command, shell=True)
            except Exception as e:
                print(f"批量安装时执行安装命令{command}时出错")
                raise e
        else:
            print("安装依赖成功")
            return True
    else:
        if PLATFORM == 'Windows':
            if config["env"] == "conda":
                if package in WINDOWS_CONDA_BLACKDICT.keys():
                    command = WINDOWS_CONDA_BLACKDICT[package].format(
                        python_path=python_path)
                else:
                    command = f"conda install -y {package} -p env"
            elif config["env"] == "env":
                if package in WINDOWS_ENV_BLACKLIST:
                    print(f"""windowsc an not install {package} through pip,
                    please go to http://www.lfd.uci.edu/~gohlke/pythonlibs and 
                    download the packages you need,then install""")
                    return False
                elif package in WINDOWS_ENV_BLACKDICT.keys():
                    command = WINDOWS_ENV_BLACKDICT[package].format(python_path=python_path)
                else:
                    command = f"{python_path} -m pip install {package}"
        else:
            if config["env"] == "env":
                command = f"{python_path} -m pip install {package}"
            elif config["env"] == "conda":
                command = f"conda install -y -p env {package}"

        try:
            subprocess.check_call(command, shell=True)
        except Exception as e:
            print(f"执行安装命令:{command}时出错")
            raise e
        else:
            print(package, "installed")
            if dev is True:
                requirement = list(set(config["requirement-dev"]))
                requirement.append(package)
                config["requirement-dev"] = requirement
            else:
                requirement = list(set(config["requirement"]))
                requirement.append(package)
                config["requirement"] = requirement
            with open(str(PMFPRC_PATH), "w") as f:
                json.dump(config, f)
            print("安装依赖成功")
            return True
