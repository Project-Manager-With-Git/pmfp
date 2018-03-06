from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def doc(argv):
    """处理项目文档的流程."""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        command = "build"
        if argv.serve:
            command = "serve"
        obj.doc(command=command)
    else:
        print("please run this command in the root of the  project, and initialise first")
