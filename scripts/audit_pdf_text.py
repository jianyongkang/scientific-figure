#!/usr/bin/env python3
"""Audit rendered PDF text sizes and font family with PyMuPDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    try:
        import fitz
    except Exception:
        print("PyMuPDF is required: python -m pip install pymupdf")
        return 2

    allowed_sizes = {7.0, 8.0, 9.0, 10.0}
    findings = []
    doc = fitz.open(args.pdf)
    for page_index, page in enumerate(doc):
        data = page.get_text("dict")
        for block in data.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = (span.get("text") or "").strip()
                    if not text:
                        continue
                    size = round(float(span.get("size", 0.0)), 1)
                    font = str(span.get("font", ""))
                    if size not in allowed_sizes:
                        findings.append({"page": page_index + 1, "type": "font-size", "text": text, "size": size})
                    normalized = font.lower().replace(" ", "")
                    if "timesnewroman" not in normalized and "timesnewromanps" not in normalized:
                        findings.append({"page": page_index + 1, "type": "font-family", "text": text, "font": font})

    result = {"pdf": str(args.pdf), "findings": findings, "pass": not findings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if findings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
