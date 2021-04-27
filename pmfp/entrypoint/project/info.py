import json
from pmfp.utils.endpoint import EndPoint
from .core import project


class InfoBase(EndPoint):
    """获取本目录下项目的基本信息."""
    verify_schema = False
    load_all_config_file = True
    config_file_only_get_need = False

    def do_main(self) -> None:
        pass


class Info(InfoBase):
    """获取本目录下项目的基本信息."""
    verify_schema = False
    load_all_config_file = True
    config_file_only_get_need = False

    def do_main(self) -> None:
        print(json.dumps(self.config, ensure_ascii=False, indent=4))


project_info = project.regist_sub(Info)
