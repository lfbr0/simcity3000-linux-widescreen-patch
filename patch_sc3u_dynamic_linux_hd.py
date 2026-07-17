#!/usr/bin/env python3
"""
Reversible SimCity 3000 Unlimited native Linux HD patch.

This patch targets the exact sc3u.dynamic binary identified by SHA-256:
d2c94405b1fbfd2ddbf6ffbdefa255587f86d19420f751e64b78d34278fce6d5

It does not overwrite the source binary. It creates sc3u.dynamic.hd.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

EXPECTED_SHA256 = "d2c94405b1fbfd2ddbf6ffbdefa255587f86d19420f751e64b78d34278fce6d5"

PATCHES = (
    # FixStartupResolutionValuesIfNeeded(...): return immediately.
    (
        0x000FFE34,
        bytes.fromhex("55 89 e5 56 8b 75 0c 8b"),
        bytes.fromhex("c3 90 90 90 90 90 90 90"),
        "disable resolution fallback rewriting",
    ),
    # IsStartupResolutionOK(...): return true immediately.
    (
        0x000FFF14,
        bytes.fromhex("55 89 e5 8b 55 0c 8b 4d"),
        bytes.fromhex("b0 01 c3 90 90 90 90 90"),
        "accept arbitrary startup resolution",
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "sc3u.dynamic")
    destination = Path(
        sys.argv[2] if len(sys.argv) > 2 else source.with_name("sc3u.dynamic.hd")
    )

    if not source.is_file():
        print(f"Error: source binary not found: {source}", file=sys.stderr)
        return 1

    data = bytearray(source.read_bytes())
    digest = sha256(data)

    if digest != EXPECTED_SHA256:
        print("Error: unsupported sc3u.dynamic build.", file=sys.stderr)
        print(f"Expected SHA-256: {EXPECTED_SHA256}", file=sys.stderr)
        print(f"Actual SHA-256:   {digest}", file=sys.stderr)
        return 1

    for offset, expected, replacement, description in PATCHES:
        actual = bytes(data[offset : offset + len(expected)])
        if actual != expected:
            print(
                f"Error: bytes at 0x{offset:x} do not match for: {description}",
                file=sys.stderr,
            )
            print(f"Expected: {expected.hex(' ')}", file=sys.stderr)
            print(f"Actual:   {actual.hex(' ')}", file=sys.stderr)
            return 1
        data[offset : offset + len(replacement)] = replacement

    destination.write_bytes(data)
    os.chmod(destination, source.stat().st_mode)

    print(f"Patched binary created: {destination}")
    print(f"Source SHA-256:  {digest}")
    print(f"Patched SHA-256: {sha256(data)}")
    print("Original binary was not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
