"""对http服务进行简单压测."""
import json
from typing import Dict, Any
from boom.boom import load, print_stats


def http_stress(config: Dict[str, Any]) -> None:
    """http简单压测并打印结果."""
    result = load(**config)
    print_stats(result)
