"""为项目创建执行环境."""
import json
import subprocess
from typing import Dict, Any
from pmfp.const import (
    GOLBAL_PYTHON_VERSION,
    ENV_PATH,
    JS_ENV_PATH,
    PROJECT_HOME
)
from .utils import new_json_package
from .const import (
    WEBPACK_BASE_CONFIG,
    WEBPACK_PROD_CONFIG,
    WEBPACK_TEST_CONFIG,
    WEBPACK_DEV_CONFIG,
    PROD_CONFIG,
    TEST_CONFIG,
    DEV_CONFIG
)


def _new_python_env(config: Dict[str, Any]):
    """为python项目创建虚拟环境.

    Args:
        config (Dict[str, Any]): 项目配置.

    Raises:
        AttributeError: unknown env

    """
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


def _new_babel(config: Dict[str, Any]):
    """初始化babel环境."""
    new_json_package(config)
    command = "npm install --save-dev babel-cli"
    subprocess.check_call(command, shell=True)
    # command = "npm install --save-dev @babel/preset-env"
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


def _new_node(config: Dict[str, Any]):
    """初始化基于babel的node环境."""
    _new_babel(config)
    with open(str(JS_ENV_PATH), encoding="utf-8") as f:
        content = json.load(f)
    with open(str(JS_ENV_PATH), "w", encoding="utf-8") as f:
        content.update({
            "babel": {
                "presets": [
                    ["env"]
                ]
            }
        })
        json.dump(content, f)


def _new_frontend(config: Dict[str, Any]):
    """初始化基于babel的前端环境."""
    _new_babel(config)
    command = "npm install --save-dev live-server"
    subprocess.check_call(command, shell=True)
    with open(str(JS_ENV_PATH), encoding="utf-8") as f:
        content = json.load(f)
    with open(str(JS_ENV_PATH), "w", encoding="utf-8") as f:
        content.update({
            "babel": {
                "presets": [
                    ["env",
                     {
                         "targets": {
                             "browsers": "> 5%"
                         }
                     }]
                ]
            }
        })
        json.dump(content, f)


def _new_webpack(config: Dict[str, Any]):
    """初始化基本webpack环境."""
    new_json_package(config)
    command = "npm install --save-dev webpack"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev webpack-cli"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev babel-core"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev babel-loader@7"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev babel-preset-env"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev style-loader"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev css-loader"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev stylus"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev stylus-loader"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev url-loader"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev file-loader"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev image-webpack-loader"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev html-webpack-plugin"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev webpack-dev-server"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev clean-webpack-plugin"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev extract-text-webpack-plugin@next"
    subprocess.check_call(command, shell=True)
    command = "npm install --save-dev uglifyjs-webpack-plugin"
    subprocess.check_call(command, shell=True)

    command = "npm install --save-dev webpack-merge"
    subprocess.check_call(command, shell=True)

    with open(str(JS_ENV_PATH), encoding="utf-8") as f:
        content = json.load(f)
    with open(str(JS_ENV_PATH), "w", encoding="utf-8") as f:
        content.update({
            "babel": {
                "presets": [
                    ["env"]
                ]
            }
        })
        json.dump(content, f)

    if not PROJECT_HOME.joinpath("env").is_dir():
        PROJECT_HOME.joinpath("env").mkdir()
    with open(str(PROJECT_HOME.joinpath("env/webpack.config.base.js")), "w", encoding="utf-8") as f:
        f.write(WEBPACK_BASE_CONFIG)
    with open(str(PROJECT_HOME.joinpath("env/webpack.config.dev.js")), "w", encoding="utf-8") as f:
        f.write(WEBPACK_DEV_CONFIG)
    with open(str(PROJECT_HOME.joinpath("env/webpack.config.prod.js")), "w", encoding="utf-8") as f:
        f.write(WEBPACK_PROD_CONFIG)
    with open(str(PROJECT_HOME.joinpath("env/webpack.config.test.js")), "w", encoding="utf-8") as f:
        f.write(WEBPACK_TEST_CONFIG)

    if not PROJECT_HOME.joinpath("env/conf").is_dir():
        PROJECT_HOME.joinpath("env/conf").mkdir()

    with open(str(PROJECT_HOME.joinpath("env/conf/dev.json")), "w", encoding="utf-8") as f:
        f.write(DEV_CONFIG)
    with open(str(PROJECT_HOME.joinpath("env/conf/prod.json")), "w", encoding="utf-8") as f:
        f.write(PROD_CONFIG)
    with open(str(PROJECT_HOME.joinpath("env/conf/test.json")), "w", encoding="utf-8") as f:
        f.write(TEST_CONFIG)


def _new_vue(config: Dict[str, Any]):
    pass


def _new_js_env(config: Dict[str, Any]):
    """为js项目创建运行环境."""
    env = config["env"]
    print('creating env')
    if JS_ENV_PATH.exists():
        print("js虚拟环境已存在!")
        return
    if env == "node":
        _new_node(config)
    elif env == "frontend":
        _new_frontend(config)
    elif env == "webpack":
        _new_webpack(config)
    elif env == "vue":
        _new_vue(config)
    else:
        raise AttributeError("unknown env")


def new_env(config: Dict[str, Any], language: str):
    """为项目创建执行环境.

    Args:
        config (Dict[str, Any]): 项目配置字典.
        language (str): 项目语言
    """

    if language in ("python", "Python"):
        _new_python_env(config)
    elif language in ("javascript", "Javascript"):
        _new_js_env(config)
        print('creating env')
    else:
        print("暂时不支持")
