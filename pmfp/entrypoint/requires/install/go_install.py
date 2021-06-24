from pathlib import Path
from typing import Optional, List
from pmfp.utils.run_command_utils import run, make_env_args


def go_install(cwd: Path,
               package_names: List[str],
               test: bool = False,
               setup: bool = False,
               extras: Optional[str] = None,
               requires: Optional[List[str]] = None,
               test_requires: Optional[List[str]] = None,
               setup_requires: Optional[List[str]] = None,
               extras_requires: Optional[List[str]] = None,
               env_args: Optional[List[str]] = None) -> None:
    envs = ["GO111MODULE::on", "GOPROXY::https://goproxy.io"]
    if env_args:
        envs += env_args
    env = make_env_args(env_args=envs)
    command_temp = "go get -u -v {req}"
    if len(package_names) > 0:
        for package_name in package_names:
            run(command_temp.format(req=package_name), cwd=cwd, env=env, visible=True, fail_exit=True)
    else:
        run("go mod tidy", cwd=cwd, env=env, visible=True, fail_exit=True)
        # if requires is not None:
        #     for req in requires:
        #         run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)
        # if test_requires is not None and test:
        #     for req in test_requires:
        #         run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)
        # if setup_requires is not None and setup:
        #     for req in setup_requires:
        #         run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)
        # if extras_requires is not None and extras:
        #     for key_req in extras_requires:
        #         _, req = key_req.split(":")
        #         run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)
