from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def build(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.build(egg=argv.egg, wheel=argv.wheel)

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
