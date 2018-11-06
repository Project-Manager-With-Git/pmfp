
import subprocess
from pmfp.const import GOLBAL_PYTHON_VERSION, ENV_PATH


def new_env(config, language):
    if language == "python":
        env = config["env"]
        print('creating env')
        if ENV_PATH.exists():
            print("虚拟环境已存在!")
            return
        if env == "env":
            python = config["global-python"]
            command = f"{python} -m venv env"
        elif env == "conda":
            command = f"conda create -y -p env python={GOLBAL_PYTHON_VERSION}"
        else:
            raise AttributeError("unknown env")
        subprocess.check_call(command, shell=True)
        print('creating python env done!')

    elif language == "javascript":
        print("暂时不支持")
        return
    else:
        print("暂时不支持")
        return
