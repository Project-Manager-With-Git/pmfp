"""添加开发环境额外依赖."""
from pathlib import Path


class InitDevRequirementMixin:
    """初始化开发环境的requirement_dev.txt."""

    def _init_dev_requirements(self)->None:
        """初始化依赖,但不会安装依赖."""
        p = Path("./requirements")
        if p.is_dir():
            with open(str(p.joinpath("requirements_dev.txt")), "w") as f:
                content = ["coverage",
                           "mypy",
                           "mypy-extensions",
                           "lxml",
                           "wheel",
                           "pydocstyle",
                           "pep8",
                           "autopep8"]
                content = [i + "\n" for i in content]
                f.writelines(content)
        else:
            raise AttributeError("_dev_requirement need dir requirements")


__all__ = ["InitDevRequirementMixin"]
