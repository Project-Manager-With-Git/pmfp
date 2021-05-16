
"""不同执行环境安装依赖."""
import warnings
from typing import List, Optional
from pmfp.utils.fs_utils import get_abs_path
from .core import requires_install, ppm_install
from .go_install import go_install
from .python_install import python_install
from .node_install import node_install


def install_requires(env: str, *,
                     package_names: Optional[List[str]] = None,
                     requirements: Optional[str] = None,
                     test: bool = False,
                     setup: bool = False,
                     extras: Optional[str] = None,
                     requires: Optional[List[str]] = None,
                     test_requires: Optional[List[str]] = None,
                     setup_requires: Optional[List[str]] = None,
                     extras_requires: Optional[List[str]] = None,
                     env_args: Optional[List[str]] = None,
                     cwd: str = ".") -> None:
    cwdp = get_abs_path(cwd)
    if not package_names:
        package_names = []
    if requirements:
        requirementsp = cwdp.joinpath(requirements)
        if requirementsp.is_file():
            with open(requirementsp, encoding="utf-8") as f:
                for line in f.readlines():
                    package = line.strip()
                    package_names.append(package)
        else:
            warnings.warn(f"路径{requirements} 不存在")
            return
    if env == "gomod":
        go_install(cwd=cwdp,
                   package_names=package_names,
                   test=test,
                   setup=setup,
                   extras=extras,
                   requires=requires,
                   test_requires=test_requires,
                   setup_requires=setup_requires,
                   extras_requires=extras_requires,
                   env_args=env_args)
    if env in ("conda", "venv"):
        python_install(cwd=cwdp, env=env,
                       package_names=package_names,
                       test=test,
                       setup=setup,
                       extras=extras,
                       requires=requires,
                       test_requires=test_requires,
                       setup_requires=setup_requires,
                       extras_requires=extras_requires,
                       env_args=env_args)
    if env in ("node", "webpack"):
        node_install(cwd=cwdp,
                     package_names=package_names,
                     test=test,
                     env_args=env_args)


requires_install.as_main(install_requires)
ppm_install.as_main(install_requires)
