from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def run(argv):
    """执行run命令的流程."""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.run(cmd=" ".join(argv.script))
    else:
        raise AttributeError(
            "please run this command in the root of the  project, and initialise first"
        )
