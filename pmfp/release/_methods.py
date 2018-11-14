from .release_js import release_js
from .release_python import release_py

def release(config):
    p_language = config["project-language"]
    if p_language in ("Javascript"):
        release_js(config=config)
    elif p_language == "Python":
        release_py(config=config)
    else:
        print("目前install子命令还不支持{p_language}语言")