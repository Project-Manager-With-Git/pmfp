"""项目的功用组件."""
import subprocess
import chardet
from typing import Dict, Any, Union, Optional
from pathlib import Path
from pmfp.const import (
    PLATFORM,
    ENV_PATH,
    PMFP_TEMPLATES_HOME,
    PROJECT_HOME
)


def get_node_version() -> Optional[str]:
    x = subprocess.run(f"node -v", capture_output=True, shell=True)
    if x.returncode == 0:
        return x.stdout.decode("utf-8").strip()[1:]


def get_golang_version() -> Optional[str]:
    x = subprocess.run(f"go version", capture_output=True, shell=True)
    if x.returncode == 0:
        return [i for i in x.stdout.decode("utf-8").strip().split(" ") if "."in i][0][2:]


def get_protoc_version() -> Optional[str]:
    x = subprocess.run(f"protoc --version", capture_output=True, shell=True)
    if x.returncode == 0:
        return [i for i in x.stdout.decode("utf-8").strip().split(" ") if "."in i][0]


def get_python_path(config: Dict[str, Any]) -> str:
    """获取python解释器的地址.

    Args:
        config (Dict[str, Any]): 项目的配置字典

    Returns:
        str: 要执行的python地址字符串

    """
    if PLATFORM == 'Windows':
        if config["env"] == "env":
            python_path = ENV_PATH.joinpath("Scripts/python")
        elif config["env"] == "conda":
            python_path = ENV_PATH.joinpath("python")
    else:
        if config["env"] == "env":
            python_path = ENV_PATH.joinpath("bin/python")
        elif config["env"] == "conda":
            python_path = ENV_PATH.joinpath("bin/python")
    return str(python_path)


def _find_template_path(language: str, t_p: str) -> Path:
    """找到项目的template地址.

    Args:
        language (str): template的语言.
        t_p (str): template名字.

    Returns:
        Path: template的地址.

    """
    category = t_p[0]
    filename = "".join(t_p[1:]) + ".json"
    file_path = PMFP_TEMPLATES_HOME.joinpath(f"{language}/{category}/{filename}")
    return file_path


def find_template_path(config: Dict[str, Any]) -> Path:
    """找到项目的template地址.

    Args:
        config (Dict[str, Any]): 项目的配置字典

    Returns:
        Path: template的地址.

    """
    language = config["project-language"]
    t_p = config["template"].split("-")
    return _find_template_path(language, t_p)


def find_project_name_path(project_name: str) -> Union[bool, Path]:
    """找到与项目同名的文件或者文件夹.

    Args:
        project_name (str): 项目名

    Returns:
        Union[bool, Path]: 找到了就返回地址,没找到返回False.

    """
    projectname_path = None
    for p in PROJECT_HOME.iterdir():
        if p.stem == project_name:
            projectname_path = p
    if projectname_path is None:
        return False
    else:
        return projectname_path
