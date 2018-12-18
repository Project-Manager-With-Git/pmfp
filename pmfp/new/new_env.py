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

def _new_node(config):
    new_json_package(config)
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

def _new_vue(config):
    pass

def _new_js_env(config):
    env = config["env"]
    print('creating env')
    if JS_ENV_PATH.exists():
        print("js虚拟环境已存在!")
        return
    if env == "node":
        _new_node(config)
    elif env == "vue":
        _new_vue(config)
    else:
        raise AttributeError("unknown env")



def new_env(config, language):
    if language == "python":
        _new_python_env(config)
    elif language == "javascript":
        _new_js_env(config)
        print('creating env')
    else:
        print("暂时不支持")
        return
