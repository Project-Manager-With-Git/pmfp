from pathlib import Path
from configparser import ConfigParser
from typing import Optional, List, Dict
from pmfp.utils.tools_info_utils import get_local_python, get_config_info
from pmfp.utils.run_command_utils import run, make_env_args


def get_req_package_name(req: str) -> str:
    if "==" in req:
        return req.split("==")[0].strip()
    elif "," in req:
        p1, _ = req.split(",")
        if ">" in p1:
            return req.split(">")[0].strip()
        elif "<" in p1:
            return req.split("<")[0].strip()
        else:
            raise AttributeError(f"can not parse {req}")
    elif ">" in req:
        return req.split(">")[0].strip()
    elif "<" in req:
        return req.split("<")[0].strip()
    else:
        return req


def get_package_with_version(pakcage_name: str, local_package: bool, cwd: Path) -> str:
    if "=" in pakcage_name:
        return pakcage_name
    if local_package:
        python_cmd = get_local_python(cwd)
        command = f"{python_cmd} -m pip show {pakcage_name}"
    else:
        command = f"pip show {pakcage_name}"
    out = run(command, cwd=cwd, visible=False, fail_exit=True)
    lines = out.splitlines()
    for line in lines:
        if "Version: " in line:
            version = line.replace("Version: ", "").strip()
            return f"{pakcage_name} >= {version}"
    else:
        return pakcage_name


def _install(package_names: List[str],
             command_temp: str,
             cwd: Path,
             env_dict: Dict[str, str],
             local_package: bool,
             config: ConfigParser,
             target_section: str,
             target_key: str) -> None:
    installed = config.get(target_section, target_key, fallback="")
    if installed == "":
        empty = True
    else:
        empty = False
    installed_lines = installed.splitlines()
    for req in package_names:
        req = req.replace(" ", "").strip()
        package_name = get_req_package_name(req)
        if "==" in req:
            run(command_temp.format(req=req), cwd=cwd, env=env_dict, visible=True, fail_exit=True)
        else:
            run(command_temp.format(req=package_name), cwd=cwd, env=env_dict, visible=True, fail_exit=True)
        pkgname = get_package_with_version(req, local_package, cwd)
        add = True
        for index, line in enumerate(installed_lines):
            if package_name in line:
                add = False
                if line.strip() == package_name:
                    installed_lines[index] = pkgname
                else:
                    installed_lines[index] = line
            else:
                installed_lines[index] = line
        if add:
            installed_lines.append(pkgname)
    new_installed = "\n".join(installed_lines)
    if empty:
        new_installed = "\n" + new_installed
    config.set(target_section, target_key, new_installed)


def python_install(cwd: Path,
                   env: str,
                   package_names: List[str],
                   test: bool = False,
                   setup: bool = False,
                   extras: Optional[str] = None,
                   requires: Optional[List[str]] = None,
                   test_requires: Optional[List[str]] = None,
                   setup_requires: Optional[List[str]] = None,
                   extras_requires: Optional[List[str]] = None,
                   env_args: Optional[List[str]] = None) -> None:
    setupcfg_path = cwd.joinpath("setup.cfg")
    config = ConfigParser()
    if setupcfg_path.exists():
        with open(setupcfg_path, encoding="utf-8") as f:
            config.read_file(f)
    pmfp_conf = get_config_info()
    env_dir = pmfp_conf["python_local_env_dir"]
    local_package = False
    if env == "conda":
        if cwd.joinpath(env_dir).is_dir():
            print("即将安装到本地环境")
            local_package = True
            command_temp = "conda install -y {req}" + f"-p {env_dir}"
        else:
            print("安装到全局环境")
            command_temp = "conda install -y {req}"
    else:
        if cwd.joinpath(env_dir).is_dir():
            print("安装到本地环境")
            local_package = True
            python_cmd = get_local_python(cwd)
            command_temp = f"{python_cmd} -m " + "pip install {req}"
        else:
            print("安装到全局环境")
            command_temp = "pip install {req}"
    env_dict = make_env_args(env_args)
    if "options" not in config.sections():
        config.add_section("options")
    if len(package_names) > 0:
        if test:
            target_section = "options"
            target_key = "tests_require"
        else:
            if setup:
                target_section = "options"
                target_key = "setup_requires"
            else:
                if extras:
                    if "options.extras_require" not in config.sections():
                        config.add_section("options.extras_require")
                    target_section = "options.extras_require"
                    target_key = extras
                else:
                    target_section = "options"
                    target_key = "install_requires"
        _install(package_names=package_names,
                 command_temp=command_temp,
                 cwd=cwd,
                 env_dict=env_dict,
                 local_package=local_package,
                 config=config,
                 target_section=target_section,
                 target_key=target_key)
    else:
        if requires:
            target_section = "options"
            target_key = "install_requires"

            _install(package_names=requires,
                     command_temp=command_temp,
                     cwd=cwd,
                     env_dict=env_dict,
                     local_package=local_package,
                     config=config,
                     target_section=target_section,
                     target_key=target_key)

        if test_requires and test:
            target_section = "options"
            target_key = "tests_require"
            _install(package_names=test_requires,
                     command_temp=command_temp,
                     cwd=cwd,
                     env_dict=env_dict,
                     local_package=local_package,
                     config=config,
                     target_section=target_section,
                     target_key=target_key)

        if setup_requires and setup:
            target_section = "options"
            target_key = "setup_requires"
            _install(package_names=setup_requires,
                     command_temp=command_temp,
                     cwd=cwd,
                     env_dict=env_dict,
                     local_package=local_package,
                     config=config,
                     target_section=target_section,
                     target_key=target_key)

        if extras_requires and extras:
            if "options.extras_require" not in config.sections():
                config.add_section("options.extras_require")
            qurs: Dict[str, List[str]] = {}
            for key_req in extras_requires:
                key, req = key_req.split(":")
                if qurs.get(key) is None:
                    qurs[key].append(req)
                else:
                    qurs[key] = [req]

            for key, reqs in qurs.items():
                target_section = "options.extras_require"
                target_key = key
                _install(package_names=reqs,
                         command_temp=command_temp,
                         cwd=cwd,
                         env_dict=env_dict,
                         local_package=local_package,
                         config=config,
                         target_section=target_section,
                         target_key=target_key)
    config.write(open(setupcfg_path, "w", newline="", encoding="utf-8"))
