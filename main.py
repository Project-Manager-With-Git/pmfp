#!/usr/bin/env python
"""PMFP.

一个项目管理脚手架.
"""

import sys

if __name__ == '__main__':
    from pmfp.entrypoint import main
    sys.exit(main(sys.argv[1:]))
