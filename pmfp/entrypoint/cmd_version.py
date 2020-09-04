"""version命令的处理."""
import json
from typing import Sequence
from pmfp import VERSION
from pmfp.const import PMFP_CONFIG_PATH
from .core import ppm


@ppm.regist_subcmd
def version(argv: Sequence[str]) -> None:
    """获取pmfp工具的版本.

    ppm version
    """
    cmd_version()


def cmd_version() -> None:
    """打印工具的版本."""
    with open(PMFP_CONFIG_PATH,"r",encoding="utf-8") as fr:
        config = json.load(fr)
    print(f"pmfp: {VERSION}")
    print(json.dumps(config,ensure_ascii=False,indent=4,sort_keys=True))
 