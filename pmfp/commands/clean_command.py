from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def clean(argv):
    """清理命令的执行流程"""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.clean(total=argv.all)
        return True
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
