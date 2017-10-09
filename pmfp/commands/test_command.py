from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def test(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.typecheck:
            obj._run_python_typecheck(html=argv.html)
        else:
            obj.test(html=argv.html)

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
