"""为项目创建文档."""
import json
import subprocess
from string import Template
from typing import Dict, Any
from pmfp.const import (
    DOC_PATH,
    PROJECT_HOME,
    PMFP_DOC_TEMP,
    JS_ENV_PATH
)
from .utils import new_json_package


def js_document(config: Dict[str, Any]):
    """为js创建文档.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    new_json_package(config)
    command = "npm install --save-dev esdoc"
    subprocess.check_call(command, shell=True)
    command = "npm install ----save-dev esdoc-publish-markdown-plugin"
    subprocess.check_call(command, shell=True)
    docs = PROJECT_HOME.joinpath("docs")
    if not docs.exists():
        docs.mkdir(parents=True, exist_ok=False)
    with open(str(JS_ENV_PATH), encoding="utf-8") as f:
        content = json.load(f)
    with open(str(JS_ENV_PATH), "w", encoding="utf-8") as f:
        content.update({
            "esdoc": {
                "destination": "./docs",
                "source": "./es",
                "includes": [r"\\.js$"],
                "excludes": [r"\\.config\\.js$"],
                "plugins": [
                    {
                        "name": "esdoc-standard-plugin"
                    }
                ]
            },
        })
        json.dump(content, f)


def default_document(config: Dict[str, Any], language: str)->bool:
    """默认的文档.

    默认使用sphinx创建文档.至少python用这个.

    Args:
        config (Dict[str, Any]): 项目配置.
        language (str): 项目的编程语言.

    Returns:
        bool: 创建成功返回True

    """
    if DOC_PATH.exists():
        print("document exists")
        return False
    else:
        package_path = PROJECT_HOME.joinpath(config["project-name"])
        project_name = config["project-name"]
        author = config["author"]
        version = config["version"]
        if package_path.exists():
            command = f"sphinx-apidoc -F -H {project_name} -A {author} -V {version} -a -o document {project_name}"
        else:
            command = f"sphinx-apidoc -F -H {project_name} -A {author} -V {version} -a -o document ."

        subprocess.check_call(command, shell=True)
        doc_conf = PMFP_DOC_TEMP.joinpath(language).open(encoding="utf-8").read()
        doc_conf_temp = Template(doc_conf)
        with open("document/conf.py", "w", encoding="utf-8") as f:
            f.write(doc_conf)
    print('building document done')
    return True


def new_document(config: Dict[str, Any], language: str):
    """初始化sphinx文档.

    Args:
        config (Dict[str, Any]): 项目配置.
        language (str): 项目的编程语言.
    """
    print('building document')
    if language == "javascript":
        js_document(config)
    else:
        default_document(config, language)
