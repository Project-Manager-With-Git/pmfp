import json
import os
import chardet
import subprocess
from typing import (
    Dict,
    Any,
    Optional
)
from pmfp.const import PMFPRC_PATH, PLATFORM


def install(
        config: Dict[str, Any],
        package: Optional[str] = None,
        dev: bool = False) -> bool:
    """python 安装依赖.

    Args:
        config (Dict[str,Any]): 现有配置
        package (Optional[str]): 依赖名,默认为None,意为安装配置中的依赖
        dev (bool): 指定安装在dev还是执行环境,默认为False
    """
    default_environ = dict(os.environ)
    env = {"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
    env.update(**default_environ)
    if package is None:
        if dev is True:
            requirement = config["requirement-dev"]
        else:
            requirement = config["requirement"]
        for package in requirement:
            command = f'go get {package}'
            res = subprocess.run(
                command,
                capture_output=True,
                shell=True,
                env=env
            )
            if res.returncode != 0:
                print(f"批量安装时执行安装命令{command}时出错")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
                break
        else:
            print("安装依赖成功")
            return True
    else:
        command = f'go get {package}'
        res = subprocess.run(
            command, 
            capture_output=True, 
            shell=True, 
            env=env
        )
        if res.returncode != 0:
            print(f"执行安装命令:{command}时出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            print(f"包{package} 安装完成!")
            if dev is True:
                requirement = list(set(config["requirement-dev"]))
                requirement.append(package)
                config["requirement-dev"] = requirement
            else:
                requirement = list(set(config["requirement"]))
                requirement.append(package)
                config["requirement"] = requirement
            with open(str(PMFPRC_PATH), "w", encoding="utf-8") as f:
                json.dump(config, f)
            print("安装并记录依赖成功")
            return True
