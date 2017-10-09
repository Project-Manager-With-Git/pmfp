from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def run(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.run(cmd=" ".join(argv.script))

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
