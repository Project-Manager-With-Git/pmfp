from pathlib import Path
from pmfp.projectinfo import ProjectInfo


def build(argv):
    """编译指令的流程"""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if not any([argv.docker, argv.egg, argv.wheel, argv.cython, argv.pyz,argv.app]):
            raise AttributeError("need a type to build")
        if argv.docker:
            obj.build_docker()
        else:
            obj.build(egg=argv.egg, wheel=argv.wheel, cython=argv.cython, pyz=argv.pyz,app=argv.app)

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
