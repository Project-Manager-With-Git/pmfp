"""为项目创建执行环境."""
import json
import subprocess
from string import Template
from typing import Dict, Any
import chardet
from pmfp.const import (
    GOLBAL_PYTHON_VERSION,
    ENV_PATH,
    JS_ENV_PATH,
    PROJECT_HOME,
    GO_ENV_PATH,
    PMFP_GOLANG_ENV_TEMP
)
from pmfp.utils import (
    get_golang_version
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
    print('创建python项目的虚拟环境')
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
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("创建python项目的虚拟环境出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print('创建python项目的虚拟环境完成!')


def _new_babel(config: Dict[str, Any]):
    """初始化babel环境."""
    new_json_package(config)
    command = "npm install --save-dev babel-cli babel-preset-env babel-register babel-polyfill mocha nyc"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("创建babel项目的环境出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print('创建babel项目的环境完成!')


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
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("创建基于babel的前端环境出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print('创建基于babel的前端环境完成!')
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
    command = "npm install --save-dev webpack webpack-cli babel-core babel-loader@7 babel-preset-env style-loader css-loader stylus stylus-loader url-loader file-loader image-webpack-loader html-webpack-plugin webpack-dev-server clean-webpack-plugin extract-text-webpack-plugin@next uglifyjs-webpack-plugin webpack-merge"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print("创建基于基本webpack的环境出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
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
    command = "vue create -b -n --preset . ."
    try:
        res = subprocess.run(command, capture_output=True, shell=True, input="Y", encoding="utf-8", text=True)
    except Exception as e:
        print(e)
        raise e
    else:
        if res.returncode != 0:
            print("创建基于基本vue-cli的环境出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            try:
                print(res.stderr.decode(encoding))
            except Exception:
                print(res.stderr)


def _new_js_env(config: Dict[str, Any]):
    """为js项目创建运行环境."""
    env = config["env"]
    print('创建js的执行环境配置')
    if JS_ENV_PATH.exists():
        print("js执行环境配置已存在!")
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


def _new_go_env(config: Dict[str, Any]):
    env = config["env"]
    print('创建go语言的编译环境')
    if GO_ENV_PATH.exists():
        print("go的虚拟环境已存在!")
        return
    project_name = config["project-name"]
    language_version = get_golang_version()
    if language_version:
        template_content = Template(
            PMFP_GOLANG_ENV_TEMP.open(encoding='utf-8').read())
        content = template_content.safe_substitute(
            project_name=project_name,
            language_version=language_version
        )
        with open(str(GO_ENV_PATH), "w", encoding="utf-8") as fa:
            fa.write(content)
    else:
        raise AttributeError("需要先安装go语言")


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
    elif language in ("go", "golang", "Go", "Golang"):
        _new_go_env(config)
    else:
        print(f"暂时不支持语言{language}创建环境")
