import re
from pathlib import Path
from argparse import Namespace
from .projectinfo import ProjectInfo

def status(args: Namespace)->bool:
    path = Path(".ppmrc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        print(obj)
        return True
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
