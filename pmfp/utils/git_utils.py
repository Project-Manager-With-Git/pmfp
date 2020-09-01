from .run_command_utils import run_command

def _git_check(p:str) -> bool:
    """检测项目有没有.git可以用于上传和打标签等操作."""
    
    if not .joinpath(".git").exists():
        return False
    else:
        return True


def _git_check_and_find_remote() -> str:
    """从项目的.git中找到远端仓库url."""
    if not _git_check():
        raise AttributeError(
            "upload to git should have a .git dir in root path")
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