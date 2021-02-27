import os
import warnings
from pathlib import Path
from typing import Optional, List
from pmfp.utils.run_command_utils import run


def go_install(cwd: Path,
               requires: Optional[List[str]] = None,
               test_requires: Optional[List[str]] = None,
               setup_requires: Optional[List[str]] = None,
               extras_requires: Optional[List[str]] = None) -> None:
    default_environ = dict(os.environ)
    env = {"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
    env.update(default_environ)
    command_temp = "go get -u -v {req}"
    if any([requires, test_requires, setup_requires, extras_requires]):
        if requires is not None:
            for req in requires:
                run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)
        if test_requires is not None:
            for req in test_requires:
                run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)
        if setup_requires is not None:
            for req in setup_requires:
                run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)
        if extras_requires is not None:
            for key_req in extras_requires:
                _, req = key_req.split(":")
                run(command_temp.format(req=req), cwd=cwd, env=env, visible=True, fail_exit=True)

    else:
        warnings.warn("请指定要安装的目标")
