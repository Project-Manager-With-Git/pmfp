from pathlib import Path
import configparser
from pmfp.projectinfo import ProjectInfo


def upload(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.upload(argv.git, argv.remote)
        return True

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
