#!/usr/bin/env python

import sys

if __name__ == '__main__':
    from pmfp.entrypoint import main
    sys.exit(main(sys.argv[1:]))
