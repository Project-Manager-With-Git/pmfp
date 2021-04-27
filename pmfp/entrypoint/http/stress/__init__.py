"""对http服务进行简单压测."""
import json
from typing import Any
from boom.boom import load, print_stats
from .core import http_stress


@http_stress.as_main
def stress_test_http(**kwargs: Any) -> None:
    """http简单压测并打印结果."""
    config_file = kwargs.get("config_file")
    if config_file:
        with open(config_file, encoding='utf-8') as f:
            c = json.load(f)
            kwargs.update(c)
        del kwargs["config_file"]
    if not kwargs.get('duration'):
        kwargs['duration'] = 0
    if not kwargs.get('data'):
        kwargs['data'] = None
    if not kwargs.get('auth'):
        kwargs['auth'] = None
    result = load(**kwargs)
    print_stats(result)
