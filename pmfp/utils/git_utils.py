from .run_command_utils import run_command
from .fs_utils import get_abs_path
def _git_check(p:str) -> bool:
    """检测项目有没有.git可以用于上传和打标签等操作."""
    root = get_abs_path(p)
    if not root.joinpath(".git").exists():
        return False
    else:
        return True


def _git_check_and_find_remote(p:str) -> str:
    """从项目的.git中找到远端仓库url."""
    if not _git_check():
        raise AttributeError(
            "git项目下需要有`.git`文件夹")
    else:
        pointgit = PROJECT_HOME.joinpath(".git")
        gitconfig = pointgit.joinpath('config')
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(str(gitconfig))
        path = parser['remote "origin"']['url']
        return path

def clone():
    pass

def push():
    pass

def tag():
    pass