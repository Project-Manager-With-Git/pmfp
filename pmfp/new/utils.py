"""new模块的通用工具."""
import json
from string import Template
from pathlib import Path
from typing import Dict, Any
from pmfp.const import (
    JS_ENV_PATH
)


def template_2_file(path: Path,**kwargs):
    """将模板转换为项目中的文件.

    Args:
        project_name (str): 项目名
        path (Path): 模板文件复制到项目中的地址
    """
    if (".py" in path.name) or (
            ".c" in path.name) or (
            ".cpp" in path.name) or (
            ".go" in path.name) or (
            "docker" in path.name) or (
            ".json" in path.name) or (
            ".mod" in path.name) or (
            ".proto" in path.name) or (
            ".js" in path.name) or (
            ".yaml" in path.name):
        try:
            template_content = Template(path.open(encoding='utf-8').read())
            content = template_content.safe_substitute(
                **kwargs
            )
        except:
            print(f"位置{path} 执行template2file出错")
            raise
        else:
            path.open("w", encoding='utf-8').write(content)
    else:
        try:
            content = path.open("r", encoding='utf-8').read()
        except UnicodeDecodeError as e:
            content = path.open("rb").read()
            path.open("wb").write(content)
        else:
            path.open("w", encoding='utf-8').write(content)
    newpath = str(path).replace(".temp", "")
    path.rename(Path(newpath))


def iter_template_2_file( project_name: str,path: Path):
    """遍历并将模板转化为项目中的文件.

    Args:
         project_name (str): 项目名
        path (Path): 模板文件复制到项目中的地址
    """
    for p in path.iterdir():
        if p.is_file():
            if p.suffix == ".temp":
                template_2_file(p,project_name=project_name)
        else:
            iter_template_2_file(project_name,p)


def new_json_package(config: Dict[str, Any]) -> None:
    """创建package.json.

    Args:
        config (Dict[str, Any]): 项目信息字典.
    """
    if not JS_ENV_PATH.exists():
        with open(str(JS_ENV_PATH), "w", encoding="utf-8") as f:
            content = {
                "name": config["project-name"],
                "version": config["version"],
                "description": config["description"],
                "author": config["author"],
                "license": config["license"]
            }
            json.dump(content, f)
