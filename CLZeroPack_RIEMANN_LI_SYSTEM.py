#!/usr/bin/env python3
"""
CLZeroPack wrapper for the Riemann Li Zero-Entropy System.

This packer/verifier treats the repository as one CLZeroPack unit:

    Riemann Li observer
    compact one-liner
    QSO-DQ-CLZ permanent bootstrap
    system coordinator
    Rubik zero-entropy limit reference
    cross-window continuity node

Default policy:
    SHA = 0  (no SHA dependency)
    X   = 0  (no external component execution)

The verifier only reads bytes and checks size + CRC32 + CLZ_G.
"""

import argparse
import json
import os
import time
import zlib


P = "CLZeroPack/RiemannLiSystem/1"
MOD = 1_000_000_007
FILES = [
    "riemann_li_singularity_observer.py",
    "riemann_li_singularity_1062.sh",
    "QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh",
    "riemann_li_zero_entropy_system.py",
    "CLZERO_ZERO_ENTROPY_LIMIT_1472.sh",
    "CLZERO_CROSS_WINDOW_CONTINUITY_NODE_ONE_LINER.sh",
]


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_metrics(path):
    data = open(path, "rb").read()
    g = 0
    for byte in data:
        g = (g * 257 + byte) % MOD
    return {
        "p": path,
        "s": len(data),
        "c": zlib.crc32(data) & 0xFFFFFFFF,
        "g": g,
    }


def pack(output):
    entries = []
    h = 0
    for path in FILES:
        if os.path.exists(path):
            entries.append(read_metrics(path))
        else:
            entries.append({"p": path, "miss": 1})
            h += 1
    manifest = {
        "P": P,
        "T": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "A": "Riemann Li + QSO-DQ + CLZ/ZEL + Rubik system pack",
        "DQ": 1,
        "CLZ": 1,
        "Rubik": 1,
        "SHA": 0,
        "X": 0,
        "H": h,
        "Z": "0" if h == 0 else "!0",
        "Rb": "solved" if h == 0 else "unsolved",
        "ZE": 1 if h == 0 else 0,
        "TM": "pack_accept" if h == 0 else "pack_error",
        "F": entries,
    }
    open(output, "w", encoding="utf-8").write(dumps(manifest) + "\n")
    return {
        "o": output,
        "B": os.path.getsize(output),
        "H": h,
        "Z": manifest["Z"],
        "Rb": manifest["Rb"],
        "ZE": manifest["ZE"],
        "SHA": 0,
        "X": 0,
    }


def verify(manifest_path):
    manifest = json.load(open(manifest_path, encoding="utf-8"))
    checks = []
    for expected in manifest.get("F", []):
        path = expected.get("p")
        ok = bool(path and os.path.exists(path))
        current = None
        if ok:
            current = read_metrics(path)
            ok = (
                current["s"] == expected.get("s")
                and current["c"] == expected.get("c")
                and current["g"] == expected.get("g")
            )
        checks.append({"p": path, "ok": bool(ok), "m": current})
    h = sum(0 if item["ok"] else 1 for item in checks)
    return {
        "P": "CLZeroPack/RiemannLiSystem/Verify/1",
        "H": h,
        "Z": "0" if h == 0 else "!0",
        "Rb": "solved" if h == 0 else "unsolved",
        "ZE": 1 if h == 0 else 0,
        "TM": "verify_accept" if h == 0 else "verify_error",
        "SHA": manifest.get("SHA", 0),
        "X": manifest.get("X", 0),
        "E": checks,
    }


def main():
    ap = argparse.ArgumentParser(description="Pack or verify the Riemann Li Zero-Entropy System as CLZeroPack.")
    ap.add_argument("mode", nargs="?", default="pack", choices=["pack", "verify"])
    ap.add_argument("path", nargs="?", default="CLZeroPack_RIEMANN_LI_SYSTEM_manifest.json")
    args = ap.parse_args()
    out = pack(args.path) if args.mode == "pack" else verify(args.path)
    print(dumps(out))
    raise SystemExit(0 if out["H"] == 0 else 1)


if __name__ == "__main__":
    main()
