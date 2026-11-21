#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261121 entry.

The poster itself is pre-rendered and committed next to this file as
entry.png. This program does no drawing: it copies that image into the
output directory the harness names through MAKEFUN_OUTPUT_DIR, checking
the copy's magic bytes, size and SHA-256 on the way so a damaged or
truncated copy can never pass as the entry. Standard library only, so it
runs in the scorer's sandbox where nothing is installed beforehand.

Run: MAKEFUN_OUTPUT_DIR=out python3 main.py  ->  out/entry.png
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "5baed0a2891c510d442de472a604c314e2f87fa2e495ced5c558ce372ca6b61f"
EXPECTED_BYTES = 227426
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("main.py: ERROR: %s" % message, file=sys.stderr)
    return 1


def digest(path):
    total = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            total.update(chunk)
    return total.hexdigest()


def checked_copy(source, destination):
    """Copy source to destination, refusing unless the copy is intact."""
    if not os.path.isfile(source):
        return fail("entry.png not found next to main.py: %s" % source)
    with open(source, "rb") as handle:
        if handle.read(len(PNG_MAGIC)) != PNG_MAGIC:
            return fail("entry.png is not a PNG file: %s" % source)
    if os.path.getsize(source) != EXPECTED_BYTES:
        return fail(
            "entry.png has %d bytes, expected %d"
            % (os.path.getsize(source), EXPECTED_BYTES)
        )
    if digest(source) != EXPECTED_SHA256:
        return fail("entry.png does not match its expected SHA-256")
    shutil.copyfile(source, destination)
    if os.path.getsize(destination) != EXPECTED_BYTES:
        return fail("copied entry.png has the wrong size: %s" % destination)
    if digest(destination) != EXPECTED_SHA256:
        return fail("copied entry.png does not match its expected SHA-256")
    return 0


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")
    status = checked_copy(source, destination)
    if status != 0:
        return status
    print("saved %s (%d bytes)" % (destination, EXPECTED_BYTES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
