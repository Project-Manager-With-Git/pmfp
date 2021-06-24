"""info命令的处理."""
import json
from pmfp.utils.endpoint import EndPoint
from pmfp.utils.tools_info_utils import get_config_info
from .core import ppm


class Info(EndPoint):
    """获取当前基本配置信息."""
    verify_schema = False

    def do_main(self) -> None:
        print(json.dumps(get_config_info(), ensure_ascii=False, indent=4))


info = ppm.regist_sub(Info)

__all__ = ["info"]
