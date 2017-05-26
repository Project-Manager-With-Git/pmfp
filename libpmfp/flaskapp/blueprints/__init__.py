__all__ = []
from importlib import import_module
from pathlib import Path
path=Path(__file__).absolute()

path = path.parent

for i in path.iterdir():
    if i.is_dir() and i.name !="__pycache__":
        mod = import_module("."+i.name,"blueprints")
        __all__ += mod.__all__
print("使用蓝图:")
print(",".join(__all__))
from blueprints.main import *
from blueprints.login import *
