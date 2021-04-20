
"""不同执行环境安装依赖."""
import sys
import json
import warnings
from pathlib import Path
from typing import Dict, Any, List, Optional
from pmfp.utils.fs_utils import get_abs_path
from .core import install
from .go_install import go_install
from .python_install import python_install


@install.as_main
def install_requires(env: str, *,
                     requires: Optional[List[str]] = None,
                     test_requires: Optional[List[str]] = None,
                     setup_requires: Optional[List[str]] = None,
                     extras_requires: Optional[List[str]] = None,
                     cwd: str = ".") -> None:
    cwdp = get_abs_path(cwd)

    if env == "gomod":
        go_install(cwd=cwdp,
                   requires=requires,
                   test_requires=test_requires,
                   setup_requires=setup_requires,
                   extras_requires=extras_requires)
    if env in ("conda", "venv"):
        python_install(cwd=cwdp, env=env,
                       requires=requires,
                       test_requires=test_requires,
                       setup_requires=setup_requires,
                       extras_requires=extras_requires)
