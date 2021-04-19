from pathlib import Path
import yaml
from .typedef import ComposeSchema


def compose_dict_to_str(compose: ComposeSchema) -> str:
    content = yaml.dump(compose, sort_keys=False)
    return content.replace("null", "").replace('"<<":', "<<:").replace("'<<':", "<<:")


def save_compose(compose: ComposeSchema, cwdp: Path, dockercompose_name: str = "docker-compose.yml") -> None:
    """保存compose为文件.

    Args:
        compose (ComposeSchema): compose字典
        cwdp (Path): 保存目录
        dockercompose_name (str, optional): compose名. Defaults to "docker-compose.yml".
    """
    content = compose_dict_to_str(compose)
    with open(cwdp.joinpath(dockercompose_name), "w", newline="", encoding="utf-8") as f:
        f.write(content)
