from .install_js import install as install_j
from .install_python import install as install_p


def install(config, kwargs):
    p_language = config["project-language"]
    if p_language in ("Javascript"):
        install_j(config=config, **kwargs)
    elif p_language == "Python":
        install_p(config=config, **kwargs)
    else:
        print("目前install子命令还不支持{p_language}语言")
