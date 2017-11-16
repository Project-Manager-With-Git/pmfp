import re
import os
import json
from pathlib import Path


class UpdateMixin:
    def update(self, version, status="dev"):
        path = Path(".").absolute()
        doc = Path('document')
        readme_rst = Path('README.rst')
        readme_md = Path('README.md')
        package = Path("package.json")
        setup = Path("setup.py")
        self.meta.version = version
        self.meta.status = status

        if readme_rst.exists():
            print("update readme.rst")
            with open(str(readme_rst), "r", encoding="utf-8") as f:
                lines = []
                for i in f:
                    if re.match(r"\* version:", i):
                        i = "* version: " + version + "\n"  # os.linesep
                    if re.match(r"\* status:", i):
                        i = "* status: " + status + "\n"  # os.linesep
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
                        i = "+ version: " + version + "\n"  # os.linesep
                    if re.match(r"\+ status:", i):
                        i = "+ status: " + status + "\n"  # os.linesep
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
                        i = "version = '" + version + "'\n"
                    lines.append(i)
            with open("document/conf.py", "w", encoding="utf-8") as f:
                for i in lines:
                    f.write(i)

            with open("document/index.rst", "r", encoding="utf-8") as f:
                lines = []
                for i in f:
                    if re.match(r"\* version:", i):
                        i = "* version: " + version + "\n"  # os.linesep
                    if re.match(r"\* status:", i):
                        i = "* status: " + status + "\n"  # os.linesep
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
                        i = "VERSION = '" + version + "'\n"
                    lines.append(i)
            with open("setup.py", "w", encoding="utf-8") as f:
                for i in lines:
                    f.write(i)
        if package.exists():
            print("update package.json")
            with open(str(package), "r") as f:
                pak = json.load(f)
            pak.update({"version": version})
            with open(str(package), "w") as f:
                json.load(pak, f)

        return True


__all__ = ["UpdateMixin"]
