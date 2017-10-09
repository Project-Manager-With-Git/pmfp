import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo

SANIC_TEMPLATE = {
    "simple": "sanic",
    "api": "sanic_api",
    "mvc": "sanic_mvc",
    "blueprints": "sanic_blueprints"
}


def sanic(argv):
    path = Path(".pmfprc")
    if path.exists():
        print("already have a .pmfprc file.")
        return False
    else:
        obj = ProjectInfo.input_info(
            template=SANIC_TEMPLATE.get(argv.template, "sanic"),
            env=argv.env,
            compiler="python",
            project_type="web",
            with_test=True,
            with_docs=False,
            with_dockerfile=True)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(install=True)
        print("init sanic application done!")
        return True