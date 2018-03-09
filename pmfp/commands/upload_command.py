from pathlib import Path
import configparser
from pmfp.projectinfo import ProjectInfo


def upload(argv):
    """上传数据命令的流程."""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.git or [] or "":
            obj.git_upload(argv.git)
        else:
            obj.upload()
        return True

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
