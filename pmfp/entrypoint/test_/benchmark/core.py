from schema_entry import EntryPoint
from ..core import test


class Benchmark(EntryPoint):
    """对指定语言的源码做性能检验."""
    argparse_noflag = "benchmark_code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["benchmark_code", "language"],
        "properties": {
            "language": {
                "type": "string",
                "description": "性能检验针对的语言",
                "enum": ["py", "go"]
            },
            "benchmark_code": {
                "type": "string",
                "description": "指定要测的测试代码"
            },
            "mem": {
                "type": "boolean",
                "description": "是否测试内存性能",
            },
            "cwd": {
                "type": "string",
                "description": "性能检验执行的位置",
                "default": "."
            }
        }
    }


test_benchmark = test.regist_sub(Benchmark)
