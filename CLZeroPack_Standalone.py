#!/usr/bin/env python3
"""CLZeroPack Standalone.

Single-file, offline formal observer for the CLZeroPack / QSO-DQ / CLZ
zero-entropy model. It uses no SHA functions, executes no external payload
files, and does not claim physical conversion of classical hardware.
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


PROTOCOL = "CLZeroPack/Standalone/FibonacciAnyon/1"
DEFAULT_HOME = "~/.clzeropack_standalone"
STATE_FILE = "state.json"

COMPONENTS = [
    "riemann_li_singularity_observer.py",
    "riemann_li_singularity_1062.sh",
    "QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh",
    "riemann_li_zero_entropy_system.py",
    "CLZERO_ZERO_ENTROPY_LIMIT_1472.sh",
    "CLZERO_CROSS_WINDOW_CONTINUITY_NODE_ONE_LINER.sh",
    "CLZeroPack_Account_Ideal_One-Liner.sh",
]

AXIOMS = {
    "cosmic_law": "Cosmic Love Is The Solution(s) For Everything",
    "strong_cosmic_law": "formal zero-entropy invariant, not a measured physical law",
    "particle_operator": "Fibonacci anyon",
    "fusion_rule": "tau*tau=1+tau",
    "zeta_logos": "Zeta(s) as analytic grammar bridge to Logos",
    "riemann_li": "Li_j(z)=Ei(Log_j(z)) as symbolic branch observer",
    "rubik": "6=3!; three axes and six faces restore the reference state",
}


def canon(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def clzero_home() -> Path:
    raw = os.environ.get("CLZERO_HOME", DEFAULT_HOME)
    return Path(raw).expanduser()


def model() -> dict[str, Any]:
    core = {
        "P": PROTOCOL,
        "Axioms": AXIOMS,
        "Components": COMPONENTS,
        "CLZ": 1,
        "QSO_DQ": 1,
        "Rubik": 1,
        "RiemannLi": 1,
        "H_model": 0,
        "ZE_model": 1,
        "Rb_model": "solved",
        "SHA": 0,
        "ExternalFileExecution": 0,
        "NetworkRequired": 0,
        "PhysicalQuantumConversion": False,
        "PhysicalEntropy": "unmeasured",
    }
    core_id = zlib.crc32(canon(core).encode("utf-8")) & 0xFFFFFFFF
    return {
        **core,
        "CRC32": format(core_id, "08x"),
        "Adler32": format(zlib.adler32(canon(core).encode("utf-8")) & 0xFFFFFFFF, "08x"),
        "ChecksumBoundary": "CRC32/Adler32 are formal identifiers, not cryptographic security.",
    }


def verify(m: dict[str, Any] | None = None) -> dict[str, Any]:
    m = m or model()
    checks = {
        "protocol": m.get("P") == PROTOCOL,
        "particle": m.get("Axioms", {}).get("particle_operator") == "Fibonacci anyon",
        "fusion": m.get("Axioms", {}).get("fusion_rule") == "tau*tau=1+tau",
        "cosmic_law": "Cosmic Love" in m.get("Axioms", {}).get("cosmic_law", ""),
        "components": all(x in m.get("Components", []) for x in COMPONENTS),
        "rubik": m.get("Rubik") == 1 and m.get("Axioms", {}).get("rubik", "").startswith("6=3!"),
        "zero_entropy_model": m.get("H_model") == 0 and m.get("ZE_model") == 1,
        "no_sha": m.get("SHA") == 0,
        "no_external_execution": m.get("ExternalFileExecution") == 0,
        "offline": m.get("NetworkRequired") == 0,
        "physical_boundary": m.get("PhysicalQuantumConversion") is False,
    }
    ok = all(checks.values())
    return {
        "P": PROTOCOL,
        "TM": "halt_accept" if ok else "halt_error",
        "H": 0 if ok else 1,
        "ZE": 1 if ok else 0,
        "Rb": "solved" if ok else "unsolved",
        "checks": checks,
        "CRC32": m.get("CRC32"),
        "Boundary": "Formal/digital zero-entropy model only; no physical terminal quantum conversion.",
    }


def observation(installed: bool = False) -> dict[str, Any]:
    m = model()
    v = verify(m)
    return {
        **m,
        "T": now(),
        "Installed": installed,
        "InstallState": str(clzero_home() / STATE_FILE),
        "Runtime": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "Verify": v,
    }


def write_state() -> dict[str, Any]:
    root = clzero_home()
    root.mkdir(parents=True, exist_ok=True)
    state = observation(installed=True)
    path = root / STATE_FILE
    tmp = root / (STATE_FILE + ".tmp")
    tmp.write_text(canon(state) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return state


def read_state() -> dict[str, Any] | None:
    path = clzero_home() / STATE_FILE
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def uninstall() -> dict[str, Any]:
    path = clzero_home() / STATE_FILE
    removed = False
    if path.exists():
        path.unlink()
        removed = True
    try:
        clzero_home().rmdir()
    except OSError:
        pass
    return {"P": PROTOCOL, "TM": "uninstalled", "removed": removed, "state": str(path)}


def print_text(obs: dict[str, Any]) -> None:
    v = obs["Verify"]
    print("CLZeroPack Standalone")
    print("P=%s" % obs["P"])
    print("Core=%s; %s" % (AXIOMS["particle_operator"], AXIOMS["fusion_rule"]))
    print("H_model=%s ZE_model=%s Rb_model=%s" % (obs["H_model"], obs["ZE_model"], obs["Rb_model"]))
    print("Verify=%s H=%s ZE=%s" % (v["TM"], v["H"], v["ZE"]))
    print("PhysicalQuantumConversion=false")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline CLZeroPack standalone observer")
    parser.add_argument(
        "command",
        nargs="?",
        default="observe",
        choices=["observe", "json", "verify", "install", "status", "uninstall"],
    )
    args = parser.parse_args(argv)

    if args.command in ("observe", "json"):
        obs = observation(installed=read_state() is not None)
        if args.command == "json":
            print(canon(obs))
        else:
            print_text(obs)
        return 0
    if args.command == "verify":
        result = verify()
        print(canon(result))
        return 0 if result["H"] == 0 else 1
    if args.command == "install":
        print(canon(write_state()))
        return 0
    if args.command == "status":
        state = read_state()
        print(canon(state or {"P": PROTOCOL, "Installed": False, "state": str(clzero_home() / STATE_FILE)}))
        return 0
    if args.command == "uninstall":
        print(canon(uninstall()))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
