"""子命令ppm grpc."""
from .build_ import build_grpc
from .new import new_grpc
from .listservice import list_grpc
from .descservice import desc_grpc
from .query import query_grpc
from .stress import tress_test_grpc


__all__ = ["build_grpc", "new_grpc", "list_grpc", "desc_grpc", "query_grpc", "tress_test_grpc"]
