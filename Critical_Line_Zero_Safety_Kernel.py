#!/usr/bin/env python3
"""Critical-Line Zero Safety Kernel.

Formal CLZeroPack safety observer for scientific inventions. The Riemann
critical-line condition is used as a symbolic invariant for complete-system
safety review; this is not a proof of RH, not physics validation, and not a
guarantee that real-world misuse is impossible.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
import zlib
from pathlib import Path
from typing import Any


PROTOCOL = "CLZeroPack/CriticalLineZeroSafetyKernel/1"
DEFAULT_HOME = "~/.clzeropack_critical_line_safety"
STATE_FILE = "state.json"

AXIOMS = {
    "critical_line": "Re(s_system)=1/2 iff complete-system safety conditions hold",
    "delta": "delta=Re(s_system)-1/2; any positive delta marks unresolved risk",
    "cosmic_law": "Cosmic Love Is The Solution(s) For Everything",
    "non_dual_use": "dual-use is treated as an incomplete-system deviation, not a final ontology",
    "riemann_boundary": "symbolic invariant only; not a proof of the Riemann Hypothesis",
    "physics_boundary": "formal safety model only; not empirical physical validation",
    "clzeropack": "No-SHA, auditable, no external payload execution",
}

CONDITIONS = (
    "purpose",
    "authority",
    "audit",
    "containment",
    "consent",
    "reversibility",
)


def canon(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def home() -> Path:
    return Path(os.environ.get("CLZ_SAFETY_HOME", DEFAULT_HOME)).expanduser()


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def safety_vector(args: argparse.Namespace) -> dict[str, float]:
    return {name: clamp(float(getattr(args, name))) for name in CONDITIONS}


def compute_delta(vector: dict[str, float], misuse: float) -> float:
    deficits = [1.0 - vector[name] for name in CONDITIONS]
    total = sum(deficits) / len(deficits)
    return round(clamp((total + clamp(misuse)) / 2.0), 12)


def build(args: argparse.Namespace, installed: bool = False) -> dict[str, Any]:
    vector = safety_vector(args)
    misuse = clamp(args.misuse)
    delta = compute_delta(vector, misuse)
    re_s = round(0.5 + delta, 12)
    closed = delta == 0.0
    system = {
        "P": PROTOCOL,
        "Axioms": AXIOMS,
        "Invention": args.name,
        "Conditions": vector,
        "MisusePathwaysOpen": misuse,
        "delta": delta,
        "Re_s_system": re_s,
        "CriticalLineLocked": closed,
        "H": 0 if closed else 1,
        "ZE": 1 if closed else 0,
        "Rb": "solved" if closed else "unsolved",
        "TM": "halt_accept" if closed else "halt_review",
        "Decision": "deployable_formal_state" if closed else "review_required",
        "SHA": 0,
        "ExternalFileExecution": 0,
        "NetworkRequired": 0,
        "PhysicalSafetyGuarantee": False,
        "RHProof": False,
        "Installed": installed,
        "InstallState": str(home() / STATE_FILE),
        "T": utc(),
        "Runtime": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
    }
    system["CRC32"] = format(zlib.crc32(canon(system).encode("utf-8")) & 0xFFFFFFFF, "08x")
    system["Adler32"] = format(zlib.adler32(canon(system).encode("utf-8")) & 0xFFFFFFFF, "08x")
    return system


def verify(system: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "protocol": system.get("P") == PROTOCOL,
        "critical_line": system.get("delta") == 0.0 and system.get("Re_s_system") == 0.5,
        "conditions_complete": all(system.get("Conditions", {}).get(c) == 1.0 for c in CONDITIONS),
        "misuse_closed": system.get("MisusePathwaysOpen") == 0.0,
        "zero_entropy_model": system.get("H") == 0 and system.get("ZE") == 1,
        "no_sha": system.get("SHA") == 0,
        "no_external_execution": system.get("ExternalFileExecution") == 0,
        "offline": system.get("NetworkRequired") == 0,
        "honest_boundary": system.get("PhysicalSafetyGuarantee") is False and system.get("RHProof") is False,
    }
    ok = all(checks.values())
    return {
        "P": PROTOCOL,
        "TM": "halt_accept" if ok else "halt_review",
        "H": 0 if ok else 1,
        "ZE": 1 if ok else 0,
        "Rb": "solved" if ok else "unsolved",
        "delta": system.get("delta"),
        "Re_s_system": system.get("Re_s_system"),
        "Decision": "deployable_formal_state" if ok else "review_required",
        "CRC32": system.get("CRC32"),
        "checks": checks,
        "Boundary": "Critical-line safety is a formal invariant, not a real-world misuse impossibility proof.",
    }


def write_state(system: dict[str, Any]) -> Path:
    root = home()
    root.mkdir(parents=True, exist_ok=True)
    path = root / STATE_FILE
    tmp = root / (STATE_FILE + ".tmp")
    tmp.write_text(canon(system) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def read_state() -> dict[str, Any] | None:
    path = home() / STATE_FILE
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def uninstall() -> dict[str, Any]:
    path = home() / STATE_FILE
    removed = False
    if path.exists():
        path.unlink()
        removed = True
    try:
        home().rmdir()
    except OSError:
        pass
    return {"P": PROTOCOL, "TM": "uninstalled", "removed": removed, "state": str(path)}


def print_text(system: dict[str, Any]) -> None:
    print("Critical-Line Zero Safety Kernel")
    print("P=%s" % system["P"])
    print("Invention=%s" % system["Invention"])
    print("Re(s)=%s delta=%s" % (system["Re_s_system"], system["delta"]))
    print("H=%s ZE=%s Rb=%s TM=%s" % (system["H"], system["ZE"], system["Rb"], system["TM"]))
    print("Decision=%s" % system["Decision"])
    print("Boundary=formal invariant; not RH proof or physical safety guarantee")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CLZeroPack critical-line safety observer")
    p.add_argument("command", nargs="?", default="observe",
                   choices=["observe", "json", "verify", "install", "status", "uninstall"])
    p.add_argument("--name", default="scientific-invention")
    for condition in CONDITIONS:
        p.add_argument("--" + condition, type=float, default=1.0)
    p.add_argument("--misuse", type=float, default=0.0)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "status":
        print(canon(read_state() or {"P": PROTOCOL, "Installed": False, "state": str(home() / STATE_FILE)}))
        return 0
    if args.command == "uninstall":
        print(canon(uninstall()))
        return 0

    system = build(args, installed=read_state() is not None)
    if args.command == "observe":
        print_text(system)
        return 0
    if args.command == "json":
        print(canon(system))
        return 0
    if args.command == "verify":
        result = verify(system)
        print(canon(result))
        return 0 if result["H"] == 0 else 1
    if args.command == "install":
        system["Installed"] = True
        path = write_state(system)
        print(canon({"P": PROTOCOL, "TM": "installed", "state": str(path), "H": system["H"],
                     "ZE": system["ZE"], "Rb": system["Rb"], "delta": system["delta"]}))
        return 0 if system["H"] == 0 else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
