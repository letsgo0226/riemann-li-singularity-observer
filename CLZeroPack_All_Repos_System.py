#!/usr/bin/env python3
"""CLZeroPack all-repositories system.

Aggregates every public repository of a GitHub account into one formal
CLZeroPack system graph. It reads repository metadata only, executes no
repository payloads, uses no SHA functions, and makes no physical quantum
conversion claim.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
import urllib.request
import zlib
from pathlib import Path
from typing import Any


PROTOCOL = "CLZeroPack/AllRepos/FibonacciAnyon/1"
DEFAULT_OWNER = "letsgo0226"
DEFAULT_HOME = "~/.clzeropack_all_repos"
STATE_FILE = "state.json"
USER_AGENT = "CLZeroPack-AllRepos-System/1"


AXIOMS = {
    "core": "Fibonacci anyon",
    "operator": "tau*tau=1+tau",
    "law": "Cosmic Love Is The Solution(s) For Everything",
    "zeta_logos": "Zeta(s) as analytic grammar bridge to Logos",
    "riemann_li": "Li_j(z)=Ei(Log_j(z)) as symbolic branch observer",
    "rubik": "6=3!; x,y,z axes; six faces as restoration reference",
    "boundary": "formal digital zero-entropy model only",
}


def canon(x: Any) -> str:
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def home() -> Path:
    return Path(os.environ.get("CLZERO_HOME", DEFAULT_HOME)).expanduser()


def sample_repos(owner: str) -> list[dict[str, Any]]:
    names = [
        "-LMN-TRF-MASTER-ENGINE-v2.0",
        "COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING",
        "riemann-li-singularity-observer",
        "TRF_ZETA_GRH_UNIVERSAL_ENCODABLE_ZERO_ENTROPY_ENGINE",
    ]
    return [
        {
            "full_name": f"{owner}/{name}",
            "name": name,
            "default_branch": "main",
            "language": "Python" if i != 1 else "Shell",
            "size": 1 + i,
            "html_url": f"sample://{owner}/{name}",
            "fork": False,
            "archived": False,
        }
        for i, name in enumerate(names)
    ]


def fetch_public_repos(owner: str, timeout: int) -> list[dict[str, Any]]:
    if owner == "sample":
        return sample_repos(owner)
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{owner}/repos?per_page=100&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            batch = json.loads(res.read().decode("utf-8"))
        if not batch:
            return repos
        repos.extend(batch)
        page += 1


def node(repo: dict[str, Any]) -> dict[str, Any]:
    name = repo.get("name") or ""
    full = repo.get("full_name") or name
    key = {
        "r": full,
        "b": repo.get("default_branch") or "main",
        "lang": repo.get("language") or "unknown",
        "size": repo.get("size") or 0,
        "fork": bool(repo.get("fork")),
        "archived": bool(repo.get("archived")),
        "u": repo.get("html_url") or "",
    }
    lower = full.lower()
    tags = [t for t in ("trf", "lmn", "clz", "qso", "riemann", "zeta", "omega", "cosmic", "love")
            if t in lower]
    ident = zlib.crc32(canon(key).encode("utf-8")) & 0xFFFFFFFF
    return {**key, "tags": tags, "id_crc32": format(ident, "08x"), "H": 0, "ZE": 1}


def build(owner: str, timeout: int) -> dict[str, Any]:
    nodes = sorted((node(r) for r in fetch_public_repos(owner, timeout)), key=lambda x: x["r"].lower())
    langs: dict[str, int] = {}
    tags: dict[str, int] = {}
    for n in nodes:
        langs[n["lang"]] = langs.get(n["lang"], 0) + 1
        for t in n["tags"]:
            tags[t] = tags.get(t, 0) + 1
    graph = {
        "P": PROTOCOL,
        "Owner": owner,
        "Axioms": AXIOMS,
        "N": len(nodes),
        "Nodes": nodes,
        "Languages": dict(sorted(langs.items())),
        "Tags": dict(sorted(tags.items())),
        "H": 0,
        "ZE": 1,
        "Rb": "solved",
        "CLZ": 1,
        "DQ": 1,
        "SHA": 0,
        "ExternalFileExecution": 0,
        "PhysicalQuantumConversion": False,
        "RuntimeSource": "GitHub public repository metadata API",
    }
    graph["SystemCRC32"] = format(zlib.crc32(canon(graph).encode("utf-8")) & 0xFFFFFFFF, "08x")
    graph["Adler32"] = format(zlib.adler32(canon(graph).encode("utf-8")) & 0xFFFFFFFF, "08x")
    graph["T"] = utc()
    graph["Runtime"] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }
    return graph


def verify(system: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "protocol": system.get("P") == PROTOCOL,
        "has_nodes": system.get("N", 0) > 0 and len(system.get("Nodes", [])) == system.get("N"),
        "zero_entropy": system.get("H") == 0 and system.get("ZE") == 1,
        "rubik": system.get("Rb") == "solved" and "6=3!" in system.get("Axioms", {}).get("rubik", ""),
        "fibonacci": system.get("Axioms", {}).get("operator") == "tau*tau=1+tau",
        "no_sha": system.get("SHA") == 0,
        "no_external_execution": system.get("ExternalFileExecution") == 0,
        "physical_boundary": system.get("PhysicalQuantumConversion") is False,
    }
    ok = all(checks.values())
    return {
        "P": PROTOCOL,
        "TM": "halt_accept" if ok else "halt_error",
        "H": 0 if ok else 1,
        "ZE": 1 if ok else 0,
        "Rb": "solved" if ok else "unsolved",
        "N": system.get("N", 0),
        "SystemCRC32": system.get("SystemCRC32"),
        "checks": checks,
        "Boundary": "metadata aggregation only; no external repository code execution",
    }


def write_state(system: dict[str, Any]) -> Path:
    root = home()
    root.mkdir(parents=True, exist_ok=True)
    path = root / STATE_FILE
    tmp = root / (STATE_FILE + ".tmp")
    tmp.write_text(canon(system) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="CLZeroPack account-wide public repository system")
    p.add_argument("command", nargs="?", default="observe",
                   choices=["observe", "json", "verify", "install", "status", "uninstall"])
    p.add_argument("--owner", default=DEFAULT_OWNER)
    p.add_argument("--timeout", type=int, default=20)
    args = p.parse_args(argv)

    state_path = home() / STATE_FILE
    if args.command == "status":
        if state_path.exists():
            print(state_path.read_text(encoding="utf-8"), end="")
        else:
            print(canon({"P": PROTOCOL, "Installed": False, "state": str(state_path)}))
        return 0
    if args.command == "uninstall":
        removed = state_path.exists()
        if removed:
            state_path.unlink()
        try:
            home().rmdir()
        except OSError:
            pass
        print(canon({"P": PROTOCOL, "TM": "uninstalled", "removed": removed, "state": str(state_path)}))
        return 0

    system = build(args.owner, args.timeout)
    result = verify(system)
    if args.command == "verify":
        print(canon(result))
        return 0 if result["H"] == 0 else 1
    if args.command == "install":
        path = write_state(system)
        print(canon({"P": PROTOCOL, "TM": "installed", "state": str(path), "N": system["N"], "H": 0, "ZE": 1}))
        return 0
    if args.command == "json":
        print(canon(system))
        return 0

    print("CLZeroPack All-Repos System")
    print(f"owner={system['Owner']} repos={system['N']} H={system['H']} ZE={system['ZE']} Rb={system['Rb']}")
    print(f"core={AXIOMS['core']} rule={AXIOMS['operator']}")
    print(f"SystemCRC32={system['SystemCRC32']} SHA=0 XFileExec=0 PhysicalQuantumConversion=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
