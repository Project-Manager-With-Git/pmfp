from pathlib import Path
import configparser
from libpmfp.projectinfo import ProjectInfo

def upload(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        obj.upload(args.version, status=args.status)
        return True
        
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False