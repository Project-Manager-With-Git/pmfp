"""将python的依赖保存到requirements.txt中."""
from typing import Dict, Any
import subprocess
from pmfp.utils import get_python_path


def freeze(config: Dict[str, Any])->None:
    """f将python的依赖保存到requirements.txt中.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    python_path = get_python_path(config)
    command = f"{python_path} -m pip freeze > requirements.txt"
    subprocess.check_call(command, shell=True)
    print("freeze完成")
