"""初始化c的执行环境."""
from pathlib import Path
from .utils import new_env_cmake


def init_c_env(cwd: Path,
               project_name: str,
               version: str,
               description: str,) -> None:
    new_env_cmake(cwd=cwd,
                  project_name=project_name,
                  version=version,
                  description=description,
                  language="C")
    print("构造c环境完成")
