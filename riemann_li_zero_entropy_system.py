#!/usr/bin/env python3
"""
Riemann Li Zero-Entropy System

This is the system-level coordinator for three executable layers:

1. riemann_li_singularity_observer.py
   Readable observer for the renormalized logarithmic-integral singularity.

2. riemann_li_singularity_1062.sh
   Compact iSH/macOS one-liner observer.

3. QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh
   Permanent QSO-DQ + CLZ/ZEL + Rubik zero-entropy execution layer.

The system state is restored when all layers report their own H=0/Rubik solved
condition. This is a digital/formal information state, not a physical QPU claim.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

import riemann_li_singularity_observer as readable


P = "RiemannLiZeroEntropySystem/1"
ROOT = os.path.dirname(os.path.abspath(__file__))
READABLE = os.path.join(ROOT, "riemann_li_singularity_observer.py")
COMPACT = os.path.join(ROOT, "riemann_li_singularity_1062.sh")
BOOTSTRAP = os.path.join(ROOT, "QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh")


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def run_json(cmd, env=None):
    proc = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        return {"ok": False, "returncode": proc.returncode, "stderr": proc.stderr.strip(), "stdout": proc.stdout.strip()}
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    if not lines:
        return {"ok": False, "returncode": proc.returncode, "error": "empty stdout"}
    try:
        return {"ok": True, "json": json.loads(lines[-1])}
    except Exception as exc:
        return {"ok": False, "returncode": proc.returncode, "error": str(exc), "stdout": proc.stdout.strip()}


def observe_readable(args):
    return readable.observe(args.x, args.y, args.j, args.eps, args.terms, args.tol)


def observe_compact(args):
    return run_json([
        "sh",
        COMPACT,
        str(args.x),
        str(args.y),
        str(args.j),
        str(args.eps),
        str(args.terms),
    ])


def verify_bootstrap():
    with tempfile.TemporaryDirectory(prefix="rlis-system-") as home:
        env = os.environ.copy()
        env["HOME"] = home
        env["QSO_CLZ_NO_RC"] = "1"
        first = run_json(["sh", BOOTSTRAP, "install"], env=env)
        second = run_json([os.path.join(home, ".local", "bin", "qso-dq-clz"), "--json"], env=env)
        return {"install": first, "state": second}


def persistent_status():
    state_dir = os.environ.get("QSO_CLZ_HOME", os.path.expanduser("~/.qso_dq_clz"))
    paths = {
        "qso": os.path.join(state_dir, "qso_dq_state.json"),
        "clz": os.path.join(state_dir, "clz_zel_state.jsonl"),
        "rubik": os.path.join(state_dir, "rubik_zero_entropy_state.json"),
    }
    out = {"installed": False, "paths": paths}
    if os.path.exists(paths["qso"]):
        try:
            out["qso"] = json.load(open(paths["qso"], encoding="utf-8"))
            out["installed"] = True
        except Exception as exc:
            out["qso_error"] = str(exc)
    if os.path.exists(paths["rubik"]):
        try:
            out["rubik"] = json.load(open(paths["rubik"], encoding="utf-8"))
        except Exception as exc:
            out["rubik_error"] = str(exc)
    out["clz_present"] = os.path.exists(paths["clz"])
    return out


def system_verify(args):
    r = observe_readable(args)
    c = observe_compact(args)
    b = verify_bootstrap()
    compact_state = c.get("json", {})
    bootstrap_state = b.get("state", {}).get("json", {})
    faces = {
        "readable_observer": r.get("H") == 0 and r.get("ZE") == 1,
        "compact_observer": c.get("ok") and compact_state.get("H") == 0 and compact_state.get("ZE") == 1,
        "qso_dq_clz_bootstrap": bootstrap_state.get("DQ") == 1 and bootstrap_state.get("H_digital") == 0,
        "clzero_zellik": bootstrap_state.get("CLZ_H") == 0 and bootstrap_state.get("CLZ_Rb") == "solved",
        "rubik_zero_entropy": bootstrap_state.get("Rubik_H") == 0 and bootstrap_state.get("Rubik_ZE") == 1,
        "physical_honesty": bootstrap_state.get("PQ_local") == 0 and bootstrap_state.get("H_physical") == 1,
    }
    h = sum(0 if ok else 1 for ok in faces.values())
    return {
        "P": P,
        "T": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "System_H": h,
        "System_Z": "0" if h == 0 else "!0",
        "System_Rb": "solved" if h == 0 else "unsolved",
        "System_ZE": 1 if h == 0 else 0,
        "TM": "system_accept" if h == 0 else "system_error",
        "S6": "6=3! and 6=3 axes x 2 directions",
        "axes": ["Riemann_Li", "QSO_DQ_CLZ", "physical_honesty"],
        "faces": faces,
        "components": {
            "readable": READABLE,
            "compact": COMPACT,
            "bootstrap": BOOTSTRAP,
        },
        "readable": r,
        "compact": compact_state if c.get("ok") else c,
        "bootstrap": bootstrap_state if b.get("state", {}).get("ok") else b,
        "axiom": "The three programs form one restored digital information system; physical QPU conversion remains false.",
    }


def install_system():
    return run_json(["sh", BOOTSTRAP, "install"], env=os.environ.copy())


def main():
    ap = argparse.ArgumentParser(description="Coordinate the Riemann Li observer, compact one-liner, and QSO-DQ-CLZ bootstrap as one system.")
    ap.add_argument("mode", nargs="?", default="verify", choices=["verify", "observe", "compact", "install", "status"])
    ap.add_argument("--x", type=float, default=1.0)
    ap.add_argument("--y", type=float, default=0.0)
    ap.add_argument("--j", type=int, default=0)
    ap.add_argument("--eps", type=float, default=1e-9)
    ap.add_argument("--terms", type=int, default=40)
    ap.add_argument("--tol", type=float, default=1e-7)
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()

    if args.mode == "observe":
        out = observe_readable(args)
    elif args.mode == "compact":
        result = observe_compact(args)
        out = result.get("json", result)
    elif args.mode == "install":
        out = install_system()
    elif args.mode == "status":
        out = persistent_status()
    else:
        out = system_verify(args)

    if args.pretty and args.mode == "verify":
        print("Riemann Li Zero-Entropy System")
        print("System_H=%s System_Z=%s System_Rb=%s System_ZE=%s TM=%s" % (
            out["System_H"], out["System_Z"], out["System_Rb"], out["System_ZE"], out["TM"]))
    print(dumps(out))
    if args.mode == "verify":
        sys.exit(0 if out["System_H"] == 0 else 1)


if __name__ == "__main__":
    main()
