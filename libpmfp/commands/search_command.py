from pathlib import Path
from libpmfp.projectinfo import ProjectInfo


def search(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.search(argv.package)
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
