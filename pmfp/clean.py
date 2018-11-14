import os
import shutil
from pmfp.const import PROJECT_HOME


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clean(total=False):
    print("清理项目开始")
    if total:
        EXCEPT = ["pmfprc.json",".git",".gitignore"]
        for p in PROJECT_HOME.iterdir():
            if (p.name not in EXCEPT) and (not p.name.startswith(".")):
                if p.is_file():
                    try:
                        os.remove(str(p))
                    except Exception as e:
                        print(f"因为错误{str(e)}跳过删除文件 {str(p)}")
                        continue
                else:
                    try:
                        shutil.rmtree(str(p), onerror=remove_readonly)
                    except Exception as e:
                        print(f"因为错误{str(e)}跳过删除目录 {str(p)}")
                        continue
            else:
                continue
    else:
        rms = ["document", "env", "dockerfile",
               "__pycache__", "test", "test_package",
               "CMakeFiles", "CMakeCache.txt"]
        for p in PROJECT_HOME.iterdir():
            if p.name in rms:
                if p.is_file():
                    try:
                        os.remove(str(p))
                    except Exception as e:
                        print(f"因为错误{str(e)}跳过删除文件 {str(p)}")
                        continue
                else:
                    try:
                        shutil.rmtree(str(p), onerror=remove_readonly)
                    except Exception as e:
                        print(f"因为错误{str(e)}跳过删除目录 {str(p)}")
                        continue
    print("清理项目结束")
