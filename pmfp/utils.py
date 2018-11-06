from pmfp.const import (
    PLATFORM,
    ENV_PATH,
    PMFP_TEMPLATES_HOME,
    PROJECT_HOME
)


def get_python_path(config):
    """获取python解释器的地址."""
    if PLATFORM == 'Windows':
        if config["env"] == "env":
            python_path = ENV_PATH.joinpath("Scripts/python")
        elif config["env"] == "conda":
            python_path = ENV_PATH.joinpath("python")
    else:
        if config["env"] == "env":
            python_path = ENV_PATH.joinpath("bin/python")
        elif config["env"] == "conda":
            python_path = ENV_PATH.joinpath("bin/python")
    return str(python_path)


def find_template_path(config):
    language = config["project-language"]
    t_p = config["template"].split("-")
    category = t_p[0]
    filename = "".join(t_p[1:]) + ".json"
    file_path = PMFP_TEMPLATES_HOME.joinpath(f"{language}/{category}/{filename}")
    return file_path


def find_project_name_path(project_name):
    projectname_path = None
    for p in PROJECT_HOME.iterdir():
        if p.stem == project_name:
            projectname_path = p
    if projectname_path is None:
        return False
    else:
        return projectname_path
