import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def new(argv):
    if argv.command == 'cython':
        ProjectInfo.init_cython(argv.name,dir_path=argv.to,math=argv.math)
        return
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.command == "document":
            obj.init_docs() 
        elif argv.command == "setup.py":
            obj.init_setup(cython=argv.with_cython, command=argv.command, math=argv.math)
        elif argv.command == "dockerfile":
            obj.init_docker()
        elif argv.command == "main":
            obj._init_main()
        else:
            print("unknown command")
            return False

        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
    else:
        print("please run this command in the root of the  project, and initialise first")
