"""更新项目版本."""
import re
import json
from pathlib import Path


class UpdateMixin:
    """更新项目版本的混入类."""

    def update(self, version: str, status: str)->None:
        """更新项目的版本或者状态.

        只能修改项目的版本和状态,其他的可以去配置文件`.pmfprc.json`

        Args:
            version (str): - 项目版本
            status (str, optional): - 项目状态

        """
        #path = Path(".").absolute()
        doc = Path('document')
        readme_rst = Path('README.rst')
        readme_md = Path('README.md')
        package = Path("package.json")
        setup = Path("setup.py")
        if not any([version,status]):
            raise AttributeError("update must have a status or a version")
        if version:
            self.meta.version = version
        if status:
            self.meta.status = status
        if readme_rst.exists():
            print("update readme.rst")
            with open(str(readme_rst), "r", encoding="utf-8") as f:
                lines = []
                for i in f:
                    if re.match(r"\* version:", i):
                        i = "* version: " + self.meta.version + "\n"  # os.linesep
                    if re.match(r"\* status:", i):
                        i = "* status: " + self.meta.status + "\n"  # os.linesep
                    lines.append(i)
            with open(str(readme_rst), "w", encoding="utf-8") as f:
                for i in lines:
                    f.write(i)
        if readme_md.exists():
            print("update readme.md")
            with open(str(readme_md), "r", encoding="utf-8") as f:
                lines = []
                for i in f:
                    if re.match(r"\+ version:", i):
                        i = "+ version: " + self.meta.version + "\n"  # os.linesep
                    if re.match(r"\+ status:", i):
                        i = "+ status: " + self.meta.status + "\n"  # os.linesep
                    lines.append(i)
            with open(str(readme_md), "w", encoding="utf-8") as f:
                for i in lines:
                    f.write(i)
        if doc.exists():
            print("update document/conf.py")
            with open("document/conf.py", "r", encoding="utf-8") as f:
                lines = []
                for i in f:
                    if re.match(r"version =", i):
                        i = "version = '" + self.meta.version + "'\n"
                    lines.append(i)
            with open("document/conf.py", "w", encoding="utf-8") as f:
                for i in lines:
                    f.write(i)

            with open("document/index.rst", "r", encoding="utf-8") as f:
                lines = []
                for i in f:
                    if re.match(r"\* version:", i):
                        i = "* version: " + self.meta.version + "\n"  # os.linesep
                    if re.match(r"\* status:", i):
                        i = "* status: " + self.meta.status + "\n"  # os.linesep
                    lines.append(i)
            with open("document/index.rst", "w", encoding="utf-8") as f:
                for i in lines:
                    f.write(i)

        if setup.exists():
            print("update setup.py")
            with open("setup.py", "r", encoding="utf-8") as f:
                lines = []
                for i in f:
                    if re.match(r"VERSION =", i):
                        i = "VERSION = '" + self.meta.version + "'\n"
                    lines.append(i)
            with open("setup.py", "w", encoding="utf-8") as f:
                for i in lines:
                    f.write(i)
        if package.exists():
            print("update package.json")
            with open(str(package), "r") as f:
                pak = json.load(f)
            pak.update({"version": self.meta.version})
            with open(str(package), "w") as f:
                json.dump(pak, f)


__all__ = ["UpdateMixin"]
