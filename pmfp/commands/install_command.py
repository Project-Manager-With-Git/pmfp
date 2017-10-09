from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def install(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if not Path("env").exists():
            obj._init_env()
        record = "requirement"
        if argv.test:
            record = "test"
        if argv.dev:
            record = "dev"
        if argv.all:
            record = "all"
        if argv.packages == "DEFAULT":
            obj.install_requirements(record=record)
        else:
            obj.install(line=argv.packages, record=record)
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
