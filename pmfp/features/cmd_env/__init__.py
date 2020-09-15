"""构造不同执行环境."""
from typing import Dict, Any, List
from pmfp.utils.run_command_utils import run_command
from .env_py import new_env_py, new_env_conda
from .env_go import new_env_go


def new_env(env: str, *,
            root: str,
            project_name: str) -> None:
    """构造不同执行环境.

    Args:
        env (str): 要初始化的项目环境.
        root (str): 虚拟环境所在的根目录.
        project_name (str): 项目名.

    """
    if env == "py":
        new_env_py(root=root, project_name=project_name)
    elif env == "conda":
        new_env_conda(root=root, project_name=project_name)
    elif env == "go":
        new_env_go(root=root, project_name=project_name)
    else:
        print(f"暂不支持初始化环境{env}")
