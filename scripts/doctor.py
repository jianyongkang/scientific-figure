#!/usr/bin/env python3
"""Check runtime prerequisites for strict scientific figures."""

from __future__ import annotations

import importlib.util
import json
import sys


def main() -> int:
    report = {"python": sys.version.split()[0]}
    try:
        import matplotlib
        from matplotlib import font_manager

        report["matplotlib"] = matplotlib.__version__
        matches = [f.name for f in font_manager.fontManager.ttflist if f.name == "Times New Roman"]
        report["times_new_roman"] = bool(matches)
    except Exception as exc:
        report["matplotlib_error"] = str(exc)
        report["times_new_roman"] = False

    report["pymupdf"] = importlib.util.find_spec("fitz") is not None
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if "matplotlib_error" in report:
        return 2
    if not report["times_new_roman"]:
        print("ERROR: Times New Roman is not installed/visible to Matplotlib.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
