"""info命令的处理."""
from pathlib import Path
from pmfp.utils.endpoint import EndPoint
from .core import ppm


class Info(EndPoint):
    """获取本目录下项目的基本信息."""
    verify_schema = False
    load_all_config_file = True
    config_file_only_get_need = False

    def do_main(self) -> None:
        print(self.config)


info = ppm.regist_sub(Info)
