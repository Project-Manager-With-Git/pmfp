"""ppm requires list命令的处理."""
import json
from pmfp.utils.endpoint import EndPoint
from .core import requires


class List(EndPoint):
    """列出已有依赖."""
    verify_schema = False

    def do_main(self) -> None:
        result = {}
        for k, v in self.config.items():
            if "require" in k:
                result[k] = v
        print(json.dumps(result, ensure_ascii=False, indent=4))


requires_list = requires.regist_sub(List)
