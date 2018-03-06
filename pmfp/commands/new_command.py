import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def new(argv):
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.command == "document":
            obj.init_docs()
        elif argv.command == "setup.py":
            obj.init_setup(dir_path=argv.to, cython=argv.cython, command=argv.command, math=argv.math)
        elif argv.command == "test":
            obj.init_test()
        elif argv.command == "dockerfile":
            obj.init_docker()
        elif argv.command == "main":
            obj.init_main()
        else:
            print("unknown command")
            return False

        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
    else:
        print("please run this command in the root of the  project, and initialise first")
