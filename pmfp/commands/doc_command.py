from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def doc(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        command = "build"
        if argv.serve:
            command = "serve"
        obj.doc(command=command)
        return True

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
