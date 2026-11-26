#!/usr/bin/env python3
"""Copy the printer's one-line comeback into the grader output directory.

Stdlib only: the grader image has no third-party libraries.
Reads entry.txt next to this file and writes it byte-identical to
$MAKEFUN_OUTPUT_DIR/entry.txt, then verifies the copy with SHA-256.
"""

import hashlib
import os
import sys
from pathlib import Path


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.txt"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    data = source.read_bytes()
    text = data.decode("utf-8")
    if not text.strip():
        print("entry.txt is empty or only whitespace", file=sys.stderr)
        return 1
    if len(text) > 240:
        print(f"entry.txt is {len(text)} characters, over the 240 limit", file=sys.stderr)
        return 1
    target = Path(out_dir) / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    copied = target.read_bytes()
    if copied != data:
        print("copy mismatch: output differs from entry.txt", file=sys.stderr)
        return 1
    print(f"copied {len(data)} bytes, sha256 {sha256_hex(data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
