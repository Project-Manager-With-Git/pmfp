from pmfp.utils.run_command_utils import run_command,get_global_python
from pmfp.utils.fs_utils import get_abs_path
def new_env_py(root:str,
        project_name:str,
        project_version:str,
        project_license:str,
        author:str,
        author_email:str,
        keywords:List[str],
        description:str):

    root_path = get_abs_path(root)
    python = get_global_python()
    command = f"{python} -m venv env"
    run_command(command,cwd=root_path)
    