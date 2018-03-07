import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo



def sanic(argv):
    """快速构建sanic项目."""
    path = Path(".pmfprc.json")
    if path.exists():
        print("already have a .pmfprc file.")
        return False
    else:
        obj = ProjectInfo.input_info(
            template=argv.template,
            env=argv.env,
            compiler="python",
            project_form="sanic")
        path = Path(".pmfprc.json")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        obj.install_requirements("all")
        obj.init_docs()
        obj.init_docker()
        print("init sanic application done!")
        return True