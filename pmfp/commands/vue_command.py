import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def vue(self, args):
    path = Path(".pmfprc")
    if path.exists():
        print("already have a .pmfprc file.")
        return False
    else:
        obj = ProjectInfo.input_info(
            template=args.template,
            env="frontend",
            compiler="node",
            project_form="vue")
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project()
        print("init node vue project done!")
        return True
