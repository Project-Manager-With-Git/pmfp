"""安装js项目的依赖."""
import json
import subprocess
import chardet
from typing import (
    Dict,
    Any,
    Optional
)
from pmfp.const import (
    JS_ENV_PATH,
    PMFPRC_PATH
)


def install_one(config: Dict[str, Any], package: str, dev: bool = False) -> None:
    """安装一个依赖.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        package (str): 要安装的包名.
        dev (bool, optional): Defaults to False. 是否作为dev依赖安装.
    """
    if not JS_ENV_PATH.is_file():
        p_language = config["project-language"]
        print(f"{p_language}项目需要先有一个package.json配置文件")
    print(f"安装依赖{package}")
    if dev is False:
        command = f"npm install {package} --save"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print(f"安装依赖{package}出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        requirement = list(set(config["requirement"]))
        requirement.append(package)
        config["requirement"] = requirement
    else:
        command = f"npm install {package} --save-dev"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print(f"安装开发依赖{package}出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        requirement = list(set(config["requirement-dev"]))
        requirement.append(package)
        config["requirement-dev"] = requirement
    with open(str(PMFPRC_PATH), "w", encoding="utf-8") as f:
        json.dump(config, f)
    print(f"安装依赖{package}成功")


def install(config: Dict[str, Any], package: Optional[str] = None, dev: bool = False) -> bool:
    """为js项目安装依赖.

    Args:
        config (Dict[str, Any]): 项目信息字典.
        package (Optional[str], optional): Defaults to None. 要安装的包名.为None则查找项目配置文件中的内容安装
        dev (bool, optional): Defaults to False. [description]

    Returns:
        bool: 正常安装则返回True

    """
    if not JS_ENV_PATH.is_file():
        p_language = config["project-language"]
        print(f"{p_language}项目需要先有一个package.json配置文件")
    if package is None:
        print("安装全部依赖")
        if dev is False:
            for i in config.get("requirement"):
                install_one(config, i)
        else:
            for i in config.get("requirement-dev"):
                install_one(config, i)
        print("安装全部依赖成功")
    else:
        install_one(config, package, dev)
    return True
