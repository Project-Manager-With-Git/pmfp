import os
import json
import warnings
from pathlib import Path
from configparser import ConfigParser
from typing import Optional, List
from pmfp.utils.run_command_utils import run
from pmfp.const import PMFP_CONFIG_DEFAULT_NAME


def python_install(cwd: Path,
                   env: str,
                   requires: Optional[List[str]] = None,
                   test_requires: Optional[List[str]] = None,
                   setup_requires: Optional[List[str]] = None,
                   extras_requires: Optional[List[str]] = None) -> None:
    setupcfg_path = cwd.joinpath("setup.cfg")
    config = ConfigParser()
    if setupcfg_path.exists():
        with open(setupcfg_path) as f:
            config.read_file(f)
    if env == "conda":
        command_temp = "conda install {req}"
    else:
        command_temp = "pip install {req}"
    if any([requires, test_requires, setup_requires, extras_requires]):
        if any([requires, test_requires, setup_requires]) and "options" not in config.sections():
            config.add_section("options")
        if extras_requires is not None and "options.extras_require" not in config.sections():
            config.add_section("options.extras_require")
        if requires:
            installed = config.get("options", "install_requires", fallback="""
    """)
            for req in requires:
                run(command_temp.format(req=req), cwd=cwd, visible=True, fail_exit=True)
                if req not in installed:
                    installed += f"""
    {req}"""
            config.set("options", "install_requires", installed)

        if test_requires:
            installed = config.get("options", "tests_require", fallback="""
    """)
            for req in test_requires:
                run(command_temp.format(req=req), cwd=cwd, visible=True, fail_exit=True)
                if req not in installed:
                    installed += f"""
    {req}"""
            config.set("options", "tests_require", installed)

        if setup_requires:
            installed = config.get("options", "setup_requires", fallback="""
    """)
            for req in setup_requires:
                run(command_temp.format(req=req), cwd=cwd, visible=True, fail_exit=True)
                if req not in installed:
                    installed += f"""
    {req}"""
            config.set("options", "setup_requires", installed)

        if extras_requires:
            for key_req in extras_requires:
                key, req = key_req.split(":")
                run(command_temp.format(req=req), cwd=cwd, visible=True, fail_exit=True)
                installed = config.get("options.extras_require", key, fallback="""
    """)
                if req not in installed:
                    installed += f"""
    {req}"""
                config.set("options.extras_require", key, installed)

        config.write(open(setupcfg_path, "w", newline="", encoding="utf-8"))
    else:
        warnings.warn("请指定要安装的目标")
