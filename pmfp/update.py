"""更新项目的版本信息."""
import re
import json
from typing import Dict, Any
from pmfp.const import PROJECT_HOME


def update_readme(config: Dict[str, Any])->None:
    """更新readme中的信息.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    readme_rst = PROJECT_HOME.joinpath('README.rst')
    readme_md = PROJECT_HOME.joinpath('README.md')
    if readme_rst.exists():
        print("update readme.rst")
        with open(str(readme_rst), "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"\* version:", i):
                    i = "* version: " + config["version"] + "\n"  # os.linesep
                if re.match(r"\* status:", i):
                    i = "* status: " + config["status"] + "\n"  # os.linesep
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
                    i = "+ version: " + config["version"] + "\n"  # os.linesep
                if re.match(r"\+ status:", i):
                    i = "+ status: " + config["status"] + "\n"  # os.linesep
                lines.append(i)
        with open(str(readme_md), "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)

def update_doc(config: Dict[str, Any])->None:
    """更新文档中index页的信息.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    doc = PROJECT_HOME.joinpath('document/index.rst')
    if doc.exists():
        print("update doc index.rst")
        with open(doc, "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"\* version:", i):
                    i = "* version: " + config["version"] + "\n"  # os.linesep
                if re.match(r"\* status:", i):
                    i = "* status: " + config["status"] + "\n"  # os.linesep
                lines.append(i)
        with open(doc, "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)

def update_package_json(config: Dict[str, Any])->None:
    """更新js项目中package.json的信息.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    package = PROJECT_HOME.joinpath("package.json")
    if package.exists():
        print("update package.json")
        with open(str(package), "r", encoding="utf-8") as f:
            pak = json.load(f)
        pak.update({"version": config["version"]})
        with open(str(package), "w", encoding="utf-8") as f:
            json.dump(pak, f)

def update_info_json(config: Dict[str, Any])->None:
    """更新项目源码中的info.json文件.

    Args:
        config (Dict[str, Any]): 项目信息字典.

    """
    project_name = config["project-name"]
    info = PROJECT_HOME.joinpath(f"{project_name}/info.py")
    if info.exists():
        print("update info.py")
        with open(str(info), "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"^VERSION", i):
                    i = f'VERSION = "{config.get("version")}"\n'
                if re.match(r"^STATUS", i):
                    i = f'STATUS = "{config.get("status")}"\n'
                lines.append(i)
        with open(str(info), "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)




def update(config: Dict[str, Any])->None:
    """更新项目的状态和版本信息.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    update_doc(config)
    update_readme(config)
    update_package_json(config)
    update_info_json(config)
