"""使用npm初始化node的执行环境."""
import json
import warnings
from pathlib import Path
from typing import Optional, List
from pmfp.utils.run_command_utils import run


def new_env_node(cwd: Path, project_name: str, version: str, description: str, author: str,
                 language: Optional[str] = None, requires: Optional[List[str]] = None,
                 test_requires: Optional[List[str]] = None) -> None:
    """初始化golang默认的虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录
        project_name (str): 项目名

    """
    if not language:
        language = "js"
    js_env_path = cwd.joinpath("package.json")
    if js_env_path.exists():
        warnings.warn("package.json已存在!")
    else:
        if language == "js":
            jsenv = {
                "name": project_name,
                "version": version,
                "description": description,
                "main": "index.js",
                "author": author,
                "license": "MIT",
                "scripts": {
                    "build": "./node_modules/.bin/babel src -d dist",
                    "test": "./node_modules/.bin/mocha --require babel-polyfill --require babel-register",
                    "coverage": "./node_modules/.bin/nyc --reporter=text npm run test"
                },
                "mocha": {
                    "require": [
                        'core-js',
                        'regenerator-runtime',
                        '@babel/register'
                    ]
                },
                "nyc": {
                    "require": [
                        "@babel/register"
                    ],
                    "reporter": [
                        "lcov",
                        "text"
                    ],
                    "sourceMap": False,
                    "instrument": False,
                    "extends": "@istanbuljs/nyc-config-babel"
                },
                "babel": {
                    "presets": [
                        ["@babel/preset-env"]
                    ],
                    "plugins": ["istanbul"]
                }
            }
            with open(js_env_path, "w", encoding="utf-8") as fw:
                json.dump(jsenv, fw, indent=4)
            run("npm install --save-dev @babel/core @babel/cli @babel/preset-env nyc mocha core-js regenerator-runtime @babel/register @istanbuljs/nyc-config-babel", cwd=cwd, visible=True, fail_exit=True)
        else:
            warnings.warn(f"未知语言{language}")
            return
        if requires:
            for i in requires:
                run(f"npm install {i}", cwd=cwd, visible=True, fail_exit=True)
        if test_requires:
            for i in test_requires:
                run(f"npm install --save-dev {i}", cwd=cwd, visible=True, fail_exit=True)
