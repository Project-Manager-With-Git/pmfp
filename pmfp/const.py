"""维护常量."""
import sys
import platform

PLATFORM = platform.system()

GOLBAL_PYTHON = "python" if PLATFORM == 'Windows' else "python3"