from pathlib import Path
import json
from pmfp.projectinfo import ProjectInfo
from boom.boom import load, print_stats



def test(argv):
    path = Path(".pmfprc")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.typecheck:
            obj._run_python_typecheck(html=argv.html)
        elif argv.stress:
            if obj.form.project_type == "web":
                with open("stress_test.json") as f:
                    pas = json.load(f)
                result = load(**pas)
                print_stats(result)
            else:
                print("stress test is for web server")
                return False
        else:
            obj.test(html=argv.html)

    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
