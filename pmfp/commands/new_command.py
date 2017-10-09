import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def new(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.command == "document":
            obj.with_docs = True
            obj._init_docs()
        elif argv.command == "setup.py":
            obj._init_setup()
        elif argv.command == "test":
            obj.with_test = True
            obj._init_test()
        elif argv.command == "dockerfile":
            obj.with_dockerfile = True
            obj._init_docker()

        elif argv.command == "main":
            obj._init_main()
        else:
            print("unknown command")
            return False

        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
