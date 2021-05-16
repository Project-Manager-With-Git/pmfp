from pathlib import Path
from typing import Optional, List
from pmfp.utils.run_command_utils import run, make_env_args


def node_install(cwd: Path,
                 package_names: List[str],
                 test: bool = False,
                 env_args: Optional[List[str]] = None) -> None:
    envs = []
    if env_args:
        envs += env_args
    env = make_env_args(env_args=envs)
    command_temp = "npm install"
    if len(package_names) > 0:
        if test:
            for package_name in package_names:
                run(command_temp + f" --save-dev {package_name}", cwd=cwd, env=env, visible=True, fail_exit=True)
        else:
            for package_name in package_names:
                run(command_temp + f" {package_name}", cwd=cwd, env=env, visible=True, fail_exit=True)

    else:
        run(command_temp, cwd=cwd, env=env, visible=True, fail_exit=True)
