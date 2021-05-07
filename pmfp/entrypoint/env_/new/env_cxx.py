"""初始化cpp的执行环境."""
from pathlib import Path
from .utils import new_env_cmake


def init_cxx_env(cwd: Path,
                 project_name: str,
                 version: str,
                 description: str,) -> None:
    new_env_cmake(cwd=cwd,
                  project_name=project_name,
                  version=version,
                  description=description,
                  language="CXX")
    print("构造c++环境完成")
