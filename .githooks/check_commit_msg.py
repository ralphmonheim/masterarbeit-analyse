#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def main(path):
    try:
        text = Path(path).read_text(encoding="utf8")
    except Exception:
        text = ""
    first_line = text.splitlines()[0] if text.splitlines() else ""
    if first_line.startswith("Release "):
        pattern = r"^Release \d+\.\d+\.\d+ - .+"
        if not re.match(pattern, first_line):
            print("ERROR: Release commit message must match: 'Release x.x.x - Summary'", file=sys.stderr)
            print("Example: Release 0.3.1 - Add plot-template examples and docs", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
    sys.exit(main(sys.argv[1]))
