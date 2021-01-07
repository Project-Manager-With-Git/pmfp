"""对http服务进行简单压测."""
import json
from typing import Any
from boom.boom import load, print_stats
from .core import http_stress

# url: str, method: str, *,
#                     requests: int = 100, concurrency: int = 10, duration: int = 0,
#                     data: Optional[str] = None, ct: str = "ext/plain",
#                     quiet: bool = False, config_file: Optional[str] = None


@http_stress.as_main
def stress_test_http(**kwargs: Any) -> None:
    """http简单压测并打印结果."""
    config = {
    }
    config_file = kwargs.get("config_file")
    if config_file:
        with open(config_file, encoding='utf-8') as f:
            c = json.load(f)
            config.update(c)
        del kwargs["config_file"]
        config.update(kwargs)

    result = load(**config)
    print_stats(result)
