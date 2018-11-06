import subprocess
from typing import (
    Dict,
    Any,
    Optional
)
from pmfp.const import JS_ENV_PATH


def install(config: Dict[str, Any], package: Optional[str]=None, dev: bool=False):
    """node 安装一条依赖."""
    if not JS_ENV_PATH.is_file():
        p_language = config["project-language"]
        print(f"{p_language}项目需要先有一个package.json配置文件")
    if package is None:
        if dev is False:
            command = "npm install --save"
        else:
            command = "npm install --save-dev"
    else:
        if dev is False:
            command = f"npm install {package} --save"
        else:
            command = f"npm install {package} --save-dev"
    subprocess.check_call(command, shell=True)
    print("安装依赖成功")
    return True
