from pathlib import Path
import json
from pmfp.projectinfo import ProjectInfo
from boom.boom import load, print_stats


def test(argv):
    """测试命令的执行流程."""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.typecheck:
            obj.run_python_typecheck(html=argv.html)
        elif argv.stress:
            if obj.form.project_form in ["sanic", "flask"]:
                with open("stress_test.json") as f:
                    pas = json.load(f)
                result = load(**pas)
                print_stats(result)
            else:
                print("stress test is for web server")
                return False
        else:
            if Path("test").exists():
                obj.test(html=argv.html, g=argv.g)
            else:
                print("this project do not have test dir")
    else:
        print("please run this command in the root of the  project, and initialise first")
        return False
