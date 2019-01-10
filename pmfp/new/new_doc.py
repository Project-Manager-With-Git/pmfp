import json
import subprocess
from string import Template
from pmfp.const import (
    DOC_PATH,
    PROJECT_HOME,
    PMFP_DOC_TEMP,
    JS_ENV_PATH
)
from .utils import new_json_package


def js_document(config):
    new_json_package(config)
    command = "npm install --save-dev esdoc"
    subprocess.check_call(command, shell=True)
    command = "npm install ----save-dev esdoc-publish-markdown-plugin"
    subprocess.check_call(command, shell=True)
    docs = PROJECT_HOME.joinpath("docs")
    if not docs.exists():
        docs.mkdir(parents=True, exist_ok=False)
    with open(str(JS_ENV_PATH),encoding="utf-8") as f:
        content = json.load(f)
    with open(str(JS_ENV_PATH), "w",encoding="utf-8") as f:
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


def default_document(config, language):
    path = DOC_PATH
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
        with open("document/conf.py", "w",encoding="utf-8") as f:
            f.write(
                doc_conf_temp.substitute(
                    project_name=project_name,
                    author=author,
                    version=version
                )
            )
    print('building document done')
    return True


def new_document(config, language):
    """初始化sphinx文档."""
    print('building document')
    if language == "javascript":
        js_document(config)
    else:
        default_document(config, language)
