"""新建python项目的setup.py文件."""
from string import Template
from typing import Dict, Any
from pmfp.const import (
    PMFP_SETUP_TEMP,
    PROJECT_HOME,
)


def new_setup(config: Dict[str, Any], language: str, name: str):
    """新建python项目的setup.py文件.

    Args:
        config (Dict[str, Any]): 项目配置字典
        language (str): 编程语言
        name (str): setup.py模板的名字
    """
    if language == "Python":
        filename = name + ".py.temp"
        tempfile = PMFP_SETUP_TEMP.joinpath(filename)
        if not tempfile.exists():
            print(f"找不到{filename}")
        else:
            print("setup.py组件")
            setup_path = PROJECT_HOME.joinpath("setup.py")
            content = tempfile.open(encoding="utf-8").read()
            setup_path.open("w", encoding="utf-8").write(content)
            # manifest
            manifest_path = PROJECT_HOME.joinpath("MANIFEST.in")
            manifest_temp = PMFP_SETUP_TEMP.joinpath("MANIFEST.in.temp")
            manifest_content = Template(manifest_temp.open(encoding="utf-8").read())
            content = manifest_content.safe_substitute(
                project_name=config["project-name"]
            )
            manifest_path.open("w", encoding="utf-8").write(content)
    else:
        print("暂时不支持")
        return
