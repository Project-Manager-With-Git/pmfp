
"""不同执行环境安装依赖."""
import sys
import json
import warnings
from pathlib import Path
from typing import Dict, Any, List, Optional
from pmfp.utils.fs_utils import get_abs_path
from .core import requires_uninstall
from .python_uninstall import python_uninstall


@requires_uninstall.as_main
def uninstall_requires(package_name: str, env: str, *, cwd: str = ".") -> None:
    cwdp = get_abs_path(cwd)
    if env in ("conda", "venv"):
        python_uninstall(cwd=cwdp, env=env, package_name=package_name)
