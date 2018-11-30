import json
import subprocess
from pmfp.const import (
    GOLBAL_PYTHON_VERSION,
    ENV_PATH,
    JS_ENV_PATH,
    PROJECT_HOME
)
from .utils import new_json_package


def _new_python_env(config):
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





def _new_es6(config):
    project_name = config["project-name"]
    command = "npm install --save-dev babel-cli"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev babel-preset-env"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev babel-register"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev babel-polyfill"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev mocha"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev nyc"
    subprocess.check_call(command, shell=True)
    with open(str(JS_ENV_PATH)) as f:
        content = json.load(f)
    with open(str(JS_ENV_PATH), "w") as f:
        content.update({
            "babel": {
                "presets": [
                    ["env"]
                ]
            }
        })
        json.dump(content, f)


def new_env(config, language):
    if language == "python":
        _new_python_env(config)

    elif language == "javascript":
        new_json_package(config)
        _new_es6(config)
        env = config["env"]
        print('creating env')
    else:
        print("暂时不支持")
        return
