from pathlib import Path
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_local_python, get_config_info


def python_uninstall(cwd: Path, package_name: str, env: str) -> None:

    pmfp_conf = get_config_info()
    env_dir = pmfp_conf["python_local_env_dir"]
    if env == "conda":
        if cwd.joinpath(env_dir).is_dir():
            print("从本地环境卸载")
            command_temp = f"conda uninstall -y {package_name}" + f"-p {env_dir}"
        else:
            print("从全局环境卸载")
            command_temp = f"conda uninstall -y {package_name}"
    else:
        if cwd.joinpath(env_dir).is_dir():
            print("从本地环境卸载")
            python_cmd = get_local_python(cwd)
            command_temp = f"{python_cmd} -m " + f"pip uninstall -y {package_name}"
        else:
            print("从全局环境卸载")
            command_temp = f"pip uninstall -y {package_name}"
    run(command_temp, cwd=cwd, visible=True, fail_exit=True)
    # 删除记录
    setupcfg_path = cwd.joinpath("setup.cfg")
    if setupcfg_path.exists():
        with open(setupcfg_path, encoding="utf-8") as f:
            lines = f.readlines()
        writelines = []
        for line in lines:
            if package_name not in line:
                writelines.append(line)
        with open(setupcfg_path, "w", newline="", encoding="utf-8") as fw:
            fw.writelines(writelines)
        print("setup.cfg 更新了依赖信息")
