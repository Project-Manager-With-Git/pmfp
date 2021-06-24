"""入口类的定义和一级入口对象."""
from schema_entry import EntryPoint


class PPM(EntryPoint):
    """项目脚手架."""


ppm = PPM()
__all__ = ["ppm"]
