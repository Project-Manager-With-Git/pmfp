"""将python的依赖保存到requirements.txt中."""
from typing import Dict, Any
import os
import subprocess
import chardet
from pmfp.utils import get_python_path
from pmfp.const import PROJECT_HOME


def freeze_with_version(config: Dict[str, Any], kwargs: Dict[str, Any]) -> None:
    """f将python的依赖保存到requirements.txt中.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    python_path = get_python_path(config)
    requirement_path = PROJECT_HOME.joinpath("requirements.txt")
    dev_requirement_path = PROJECT_HOME.joinpath("requirements-dev.txt")
    all_requirement_path = PROJECT_HOME.joinpath("requirements-all.txt")
    command = f"{python_path} -m pip freeze > {str(all_requirement_path)}"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print(f"freeze出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
        print("直接写入")
        content = config.get("requirement-dev") + config.get("requirement")
        to_write = [line + "/n" for line in content]
        with open(str(all_requirement_path), "w") as f:
            f.writelines(to_write)

    if not kwargs.get("all"):
        if kwargs.get("dev"):
            content = config.get("requirement-dev")
        else:
            content = config.get("requirement")
        to_write = []
        with open(str(all_requirement_path), "r") as f:
            for line in f:
                package_name, *_ = line.split("==")
                if package_name in content:
                    to_write.append(line)
        try:
            os.remove(str(all_requirement_path))
        except Exception as e:
            print(f"因为错误{str(e)}跳过删除文件 {str(all_requirement_path)}")

        if kwargs.get("dev"):
            with open(str(dev_requirement_path), "w") as f:
                f.writelines(to_write)
        else:
            with open(str(requirement_path), "w") as f:
                f.writelines(to_write)

    print("freeze完成")


def freeze_without_version(config: Dict[str, Any], kwargs: Dict[str, Any]) -> None:
    """f将python的依赖保存到requirements.txt中.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    python_path = get_python_path(config)
    requirement_path = PROJECT_HOME.joinpath("requirements.txt")
    dev_requirement_path = PROJECT_HOME.joinpath("requirements-dev.txt")
    all_requirement_path = PROJECT_HOME.joinpath("requirements-all.txt")
    if kwargs.get("all"):
        content = config.get("requirement-dev") + config.get("requirement")
        p = all_requirement_path
    else:
        if kwargs.get("dev"):
            content = config.get("requirement-dev")
            p = dev_requirement_path
        else:
            content = config.get("requirement")
            p = requirement_path

    to_write = [line + "\n" for line in content]
    with open(str(p), "w") as f:
        f.writelines(to_write)
    print("freeze完成")


def freeze(config: Dict[str, Any], kwargs: Dict[str, Any]) -> None:
    """f将python的依赖保存到requirements.txt中.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    if kwargs.get("noversion"):
        freeze_without_version(config, kwargs)
    else:
        freeze_with_version(config, kwargs)
