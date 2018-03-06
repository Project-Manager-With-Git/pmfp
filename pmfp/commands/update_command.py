import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def update(args):
    """更新项目版本的的流程."""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.update(args.version, status=args.status)
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
