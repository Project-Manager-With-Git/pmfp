"""不同执行环境安装依赖."""
from pmfp.utils.fs_utils import get_abs_path
from .core import requires_uninstall, ppm_uninstall
from .python_uninstall import python_uninstall


def uninstall_requires(package_name: str, env: str, *, cwd: str = ".") -> None:
    cwdp = get_abs_path(cwd)
    if env in ("conda", "venv"):
        python_uninstall(cwd=cwdp, env=env, package_name=package_name)


requires_uninstall.as_main(uninstall_requires)
ppm_uninstall.as_main(uninstall_requires)
