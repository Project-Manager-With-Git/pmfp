import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def celery(argv):
    path = Path(".pmfprc")
    if path.exists():
        print("already have a .pmfprc file.")
        return False
    else:
        obj = ProjectInfo.input_info(
            template="celery",
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
        print("init celery application done!")
        return True
