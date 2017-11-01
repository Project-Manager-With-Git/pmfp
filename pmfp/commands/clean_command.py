from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def clean(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.clean(all=argv.all)
        return True
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
