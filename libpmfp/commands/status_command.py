from pathlib import Path
from libpmfp.projectinfo import ProjectInfo


def status()->bool:
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        print(obj)
        return True
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
