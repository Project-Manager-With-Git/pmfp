from pathlib import Path
from typing import List
from pmfp.utils.fs_utils import get_abs_path


def _find_pypackage(final_path: Path, packs: List[str]) -> None:
    has_init = False
    for i in final_path.iterdir():
        if i.name == "__init__.py":
            has_init = True
    if not has_init:
        return
    else:
        lates_p = final_path.name
        packs.append(lates_p)
        _find_pypackage(final_path.parent, packs)


def find_pypackage_string(to_path: str) -> str:
    """find_pypackage_string.

    Args:
        to_path (str): 目标地址
    Returns:
        str: package地址

    """
    packs: List[str] = []
    final_path = get_abs_path(to_path)
    _find_pypackage(final_path, packs)
    packstr = ".".join(reversed(packs))
    return packstr
