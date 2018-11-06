import subprocess
from string import Template
from pmfp.const import DOC_PATH, PROJECT_HOME, PMFP_DOC_TEMP


def new_document(config, language):
    """初始化sphinx文档."""
    print('building document')
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
        doc_conf = PMFP_DOC_TEMP.joinpath(language).open().read()
        doc_conf_temp = Template(doc_conf)
        with open("document/conf.py", "w") as f:
            f.write(
                doc_conf_temp.substitute(
                    project_name=project_name,
                    author=author,
                    version=version
                )
            )
    print('building document done')
    return True
