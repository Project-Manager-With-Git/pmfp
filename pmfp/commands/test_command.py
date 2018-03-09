from pathlib import Path
import json
from pmfp.projectinfo import ProjectInfo

WEB_STRESS_TEST = dict(
    url="http://localhost:5000/",
    requests=100,
    concurrency=10,
    duration=0,
    method="GET",
    data=None,
    ct='text/plain',
    auth=None,
    headers=None,
    pre_hook=None,
    post_hook=None,
    quiet=False)


def test(argv):
    """测试命令的执行流程."""
    path = Path(".pmfprc.json")
    if path.exists():
        obj = ProjectInfo.from_json(str(path))
        if argv.typecheck:
            obj.run_python_typecheck(html=argv.html)
        elif argv.stress:
            if obj.form.project_form in ["sanic", "flask"] or (
                obj.form.project_form == "script" and obj.form.template in (
                    "sanic", 'flask')):
                stress_test_path = Path("stress_test.json")
                if not stress_test_path.exists():
                    with open(str(stress_test_path), "w") as f:
                        json.dump(WEB_STRESS_TEST, f)
                from boom.boom import load, print_stats
                with open(str(stress_test_path)) as f:
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
