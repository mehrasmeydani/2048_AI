#!/usr/bin/env python3

import os
import sys


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO_ROOT, "src", "python"))

from agent2048.runtime import main


if __name__ == "__main__":
	raise SystemExit(main())
