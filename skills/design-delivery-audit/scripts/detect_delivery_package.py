#!/usr/bin/env python3
"""Check whether delivery sources are eligible for a full design audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


HTML_EXTENSIONS = {".html", ".htm"}
CSS_EXTENSIONS = {".css", ".scss", ".sass", ".less", ".styl", ".stylus"}
JAVASCRIPT_EXTENSIONS = {".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx"}
IGNORED_DIRECTORIES = {".git", ".svn", "node_modules", "__MACOSX"}


def scan(root: Path) -> dict[str, object]:
    groups: dict[str, list[str]] = {"html": [], "css": [], "javascript": []}
    fingerprint = hashlib.sha256()
    readable_count = 0
    scan_errors: list[str] = []

    def record_walk_error(error: OSError) -> None:
        scan_errors.append(str(error))

    for current_root, directory_names, file_names in os.walk(
        root, followlinks=False, onerror=record_walk_error
    ):
        directory_names[:] = sorted(
            name for name in directory_names if name not in IGNORED_DIRECTORIES
        )
        current = Path(current_root)
        for file_name in sorted(file_names):
            path = current / file_name
            relative = path.relative_to(root).as_posix()
            try:
                file_mode = path.stat().st_mode
            except OSError as error:
                scan_errors.append(f"{relative}: {error}")
                continue

            if not stat.S_ISREG(file_mode):
                continue

            try:
                with path.open("rb") as stream:
                    fingerprint.update(relative.encode("utf-8"))
                    fingerprint.update(b"\0")
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        fingerprint.update(chunk)
            except OSError as error:
                scan_errors.append(f"{relative}: {error}")
                continue

            readable_count += 1
            fingerprint.update(b"\0")

            extension = path.suffix.lower()
            if extension in HTML_EXTENSIONS:
                groups["html"].append(relative)
            if extension in CSS_EXTENSIONS:
                groups["css"].append(relative)
            if extension in JAVASCRIPT_EXTENSIONS:
                groups["javascript"].append(relative)

    if scan_errors:
        raise OSError("; ".join(scan_errors))

    source_eligible = bool(groups["html"] and (groups["css"] or groups["javascript"]))
    return {
        "root": str(root.resolve()),
        "source_eligible": source_eligible,
        "rule": "html && (css || javascript)",
        "package_fingerprint": fingerprint.hexdigest(),
        "readable_file_count": readable_count,
        "files": groups,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether page delivery sources meet full-audit file requirements."
    )
    parser.add_argument("root", help="Delivery package root directory")
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    if not root.exists() or not root.is_dir():
        print(
            json.dumps(
                {"error": "delivery root is not a directory", "root": str(root)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    try:
        result = scan(root)
    except OSError as error:
        print(
            json.dumps(
                {"error": "delivery package scan failed", "detail": str(error)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["source_eligible"] else 3


if __name__ == "__main__":
    sys.exit(main())
