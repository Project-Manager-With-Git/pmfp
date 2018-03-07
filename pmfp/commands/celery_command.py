import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def celery(argv):
    path = Path(".pmfprc.json")
    if path.exists():
        print("already have a .pmfprc file.")
        return False
    else:
        obj = ProjectInfo.input_info(
            template="simple",
            env=argv.env,
            compiler="python",
            project_form="celery")
        path = Path(".pmfprc.json")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        obj.install_requirements("all")
        obj.init_docs()
        obj.init_docker()
        print("init celery application done!")
        return True
