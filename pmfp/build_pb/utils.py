"""对应的工具."""
from pathlib import Path
from typing import List, Optional
from pmfp.const import PROJECT_HOME


def _find_pypackage(final_path: Path, packs: List[Optional[str]]):
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
    packs = []
    final_path = PROJECT_HOME.joinpath(to_path)
    _find_pypackage(final_path, packs)
    packs = ".".join(reversed(packs))
    return packs


def find_py_grpc_pb2_import_string(n: str):
    """python的grpc模块as的内容."""
    org = f"{n}_pb2"
    return "__".join(org.split("_"))
