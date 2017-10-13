import sys
from pathlib import Path
file_path = Path(__file__)
target_pyz_path = file_path.parent.parent.joinpath("black_box.pyz")
target_project_path = file_path.parent.parent.joinpath("black_box")
if target_pyz_path.exists():
    target = str(target_pyz_path)
else:
    target = str(target_project_path)
sys.path.insert(0, target)

from app_creater import create_app
from config import choose_conf

app = create_app(choose_conf("default"))

