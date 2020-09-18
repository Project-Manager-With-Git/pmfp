"""初始化python的执行环境."""
import warnings
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.fs_utils import get_abs_path, get_global_python
from pmfp.const import GOLBAL_PYTHON_VERSION


def new_env

def new_env_py(root: str,
               project_name: str) -> None:
    """初始化python默认的虚拟环境.

    Args:
        root (str): 虚拟环境所在的根目录
        project_name (str): 项目名

    """
    root_path = get_abs_path(root)
    env_path = root_path.joinpath("env")
    if env_path.exists():
        warnings.warn("python的虚拟环境已存在!")
    else:
        python = get_global_python()
        command = f"{python} -m venv env"
        run_command(command, cwd=root_path)


def new_env_conda(root: str,
                  project_name: str) -> None:
    """初始化anaconda的python虚拟环境.

    Args:
        root (str): 虚拟环境所在的根目录
        project_name (str): 项目名

    """
    root_path = get_abs_path(root)
    env_path = root_path.joinpath("env")
    if env_path.exists():
        warnings.warn("anaconda的虚拟环境已存在!")
    else:
        command = f"conda create -y -p env python={GOLBAL_PYTHON_VERSION}"
        run_command(command, cwd=root_path)
