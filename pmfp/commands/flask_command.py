import json
from pathlib import Path
from pmfp.projectinfo import ProjectInfo

FLASK_TEMPLATE = {
    "simple": "flask",
    "admin": 'flask_admin',
    "socketio": "flask_socketio",
    "api": "flask_api",
    "mvc": "flask_mvc",
    "blueprints": "flask_blueprints",
    "api_blueprints": "flask_api_blueprints"
}


def flask(argv):
    path = Path(".pmfprc")
    if path.exists():
        print("already have a .pmfprc file.")
        return False
    else:

        obj = ProjectInfo.input_info(
            template=FLASK_TEMPLATE.get(argv.template, "flask"),
            env=argv.env,
            compiler="python",
            project_type="web",
            with_test=True if argv.template in ('admin', 'mvc') else True,
            with_docs=False,
            with_dockerfile=True)
        path = Path(".pmfprc")
        with open(str(path), "w") as f:
            json.dump(obj.to_dict(), f)
        obj.init_project(install=True)
        print("init flask application done!")
        return True
