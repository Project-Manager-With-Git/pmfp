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
import chardet
from .utils import new_json_package


def js_document(config: Dict[str, Any]):
    """为js创建文档.

    Args:
        config (Dict[str, Any]): 项目配置.
    """
    new_json_package(config)
    command = "npm install --save-dev esdoc"
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print(f"安装开发js文档所需依赖esdoc出错")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        command = "npm install --save-dev esdoc-publish-markdown-plugin"
        if res.returncode != 0:
            print(f"安装开发js文档所需依赖esdoc-publish-markdown-plugin出错")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
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


def default_document(config: Dict[str, Any], language: str) -> bool:
    """默认的文档.

    默认使用sphinx创建文档.至少python用这个.

    Args:
        config (Dict[str, Any]): 项目配置.
        language (str): 项目的编程语言.

    Returns:
        bool: 创建成功返回True

    """
    if DOC_PATH.exists():
        print("document文件夹已存在")
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
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print(f"生成api文档失败")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            doc_conf = PMFP_DOC_TEMP.joinpath(language).open(encoding="utf-8").read()
            #doc_conf_temp = Template(doc_conf)
            with open("document/conf.py", "w", encoding="utf-8") as f:
                f.write(doc_conf)
            print('完成初始化文档源文件')
            print("编译项目文档")
            command = "sphinx-build -b html document docs"
            res = subprocess.run(command, capture_output=True, shell=True)
            if res.returncode != 0:
                print(f"编译项目文档失败")
                encoding = chardet.detect(res.stderr).get("encoding")
                print(res.stderr.decode(encoding))
            else:
                docs = PROJECT_HOME.joinpath("docs")
                nojekyll = docs.joinpath(".nojekyll")
                if not nojekyll.exists():
                    with nojekyll.open("w", encoding="utf-8") as f:
                        pass
                print("编译项目文档完成!")
                print("初始化项目文档国际化部分")
                command = "sphinx-build -b gettext document docs/locale"
                res = subprocess.run(command, capture_output=True, shell=True)
                if res.returncode != 0:
                    print(f"构造待翻译文件失败")
                    encoding = chardet.detect(res.stderr).get("encoding")
                    print(res.stderr.decode(encoding))
                else:
                    command = "sphinx-intl update -p docs/locale -d document/locale -l zh -l en"
                    res = subprocess.run(command, capture_output=True, shell=True)
                    if res.returncode != 0:
                        print(f"更新待翻译文件失败")
                        encoding = chardet.detect(res.stderr).get("encoding")
                        print(res.stderr.decode(encoding))
                    else:
                        print("初始化项目文档国际化部分 完成!")
            print('创建项目文档完成')
    return True


def new_document(config: Dict[str, Any], language: str):
    """初始化sphinx文档.

    Args:
        config (Dict[str, Any]): 项目配置.
        language (str): 项目的编程语言.
    """
    print('创建项目文档')
    if language == "javascript":
        js_document(config)
    else:
        default_document(config, language)
