import os
import http.server
import socketserver
import subprocess
from pmfp.utils import find_project_name_path
from pmfp.const import PROJECT_HOME


def _build_doc(config):
    project_name = config["project-name"]
    project_name_path = find_project_name_path(project_name)
    if project_name_path is False:
        print("未找到项目名同名的文件或文件夹")
        return
    if config['project-language'] == "Python":
        if project_name_path.is_file():
            print("building apidoc")
            command = f"sphinx-apidoc -o document {project_name}.py"
            subprocess.check_call(command, shell=True)
            print("build apidoc done!")
        else:
            print("building apidoc")
            command = f"sphinx-apidoc -o document {project_name}"
            subprocess.check_call(command, shell=True)
            print("build apidoc done!")

        print("building document")
        command = "sphinx-build -b html document docs"
        subprocess.check_call(command, shell=True)
        print("build Document done!")
        docs = PROJECT_HOME.joinpath("docs")
        nojekyll = docs.joinpath(".nojekyll")
        if not nojekyll.exists():
            with nojekyll.open("w") as f:
                pass
        return True


def _serve_doc(config):
    _build_doc(config)
    os.chdir("./docs")
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
    return True


def doc(config, kwargs):
    if kwargs["serve"]:
        _serve_doc(config)
    else:
        _build_doc(config)
