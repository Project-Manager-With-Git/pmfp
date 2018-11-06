from .js_test import run_js_test
from .python_test import run_python_test
def test(config,kwargs):
    html = kwargs["html"]
    typecheck = kwargs["typecheck"]
    source = kwargs["source"]
    language = config["project-language"]
    if language == "Python":
        run_python_test(config,html,typecheck,source)
        return True

    elif language == "Javascript":
        run_js_test()
        return True
    else:
        print("未知的编程语言!")
        return False