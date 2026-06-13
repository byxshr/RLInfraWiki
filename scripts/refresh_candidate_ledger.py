#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable, str(Path(__file__).with_name("build_candidate_ledger.py")), *sys.argv[1:]]))
