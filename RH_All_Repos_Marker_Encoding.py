#!/usr/bin/env python3
"""RH All-Repos Marker Encoding.

Encodes every public repository of a GitHub account as a prime-index marker
node C_n+n*i with C_n=P_n by default. Optional injected deviations demonstrate
when the marker rule enters halt_review. Repository metadata is read only; no
repository payload is executed and no RH proof is claimed.
"""

from __future__ import annotations

import argparse
import json
import math
import time
import urllib.request
import zlib
from typing import Any


PROTOCOL = "CLZeroPack/RHAllReposMarkerEncoding/1"
DEFAULT_OWNER = "letsgo0226"
USER_AGENT = "CLZeroPack-RH-AllRepos-Marker/1"


def canon(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for d in range(3, int(math.isqrt(n)) + 1, 2):
        if n % d == 0:
            return False
    return True


def first_primes(count: int) -> list[int]:
    primes: list[int] = []
    n = 2
    while len(primes) < count:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes


def primes_to(limit: int) -> list[int]:
    return [n for n in range(2, max(2, limit) + 1) if is_prime(n)]


def sample_repos(owner: str) -> list[dict[str, Any]]:
    names = [
        "CLZeroPack",
        "COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING",
        "riemann-li-singularity-observer",
        "TRF_ZETA_GRH_UNIVERSAL_ENCODABLE_ZERO_ENTROPY_ENGINE",
    ]
    return [
        {
            "full_name": f"{owner}/{name}",
            "name": name,
            "default_branch": "main",
            "language": "Python" if i % 2 == 0 else "Shell",
            "size": i + 1,
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


def interval_witnesses(c_marker: int, n: int, enough: int) -> tuple[list[dict[str, int]], bool]:
    prime_list = primes_to(max(enough, c_marker, 32))
    pmap = {p: i + 1 for i, p in enumerate(prime_list)}
    found = [p for p in range(c_marker // 2 + 1, c_marker) if is_prime(p)]
    mapped = [{"P_m": p, "m": pmap[p]} for p in found if p in pmap]
    return mapped, any(x["m"] == n for x in mapped)


def encode_repo(repo: dict[str, Any], n: int, p_n: int, marker: int, enough: int) -> dict[str, Any]:
    key = {
        "r": repo.get("full_name") or repo.get("name") or "",
        "b": repo.get("default_branch") or "main",
        "lang": repo.get("language") or "unknown",
        "size": repo.get("size") or 0,
        "fork": bool(repo.get("fork")),
        "archived": bool(repo.get("archived")),
        "u": repo.get("html_url") or "",
    }
    ok = marker == p_n
    witnesses, m_eq_n = interval_witnesses(marker, n, enough) if not ok else ([], False)
    return {
        **key,
        "n": n,
        "P_n": p_n,
        "C_n": marker,
        "z_marker": f"{marker}+{n}i",
        "C_n_equals_P_n": ok,
        "m_equals_n_possible": m_eq_n,
        "IndexPreservingCollision": (not ok) and m_eq_n,
        "TheoremGap": (not ok) and not m_eq_n,
        "IntervalPrimes": witnesses,
        "repo_crc32": format(zlib.crc32(canon(key).encode("utf-8")) & 0xFFFFFFFF, "08x"),
        "H": 0 if ok else 1,
        "ZE": 1 if ok else 0,
    }


def build(owner: str, timeout: int, inject_index: int | None, inject_c: int | None) -> dict[str, Any]:
    repos = sorted(fetch_public_repos(owner, timeout), key=lambda r: (r.get("full_name") or "").lower())
    primes = first_primes(len(repos))
    enough = max(primes[-1] if primes else 32, inject_c or 32)
    nodes = []
    for i, repo in enumerate(repos, start=1):
        marker = primes[i - 1]
        if inject_index == i and inject_c is not None:
            marker = inject_c
        nodes.append(encode_repo(repo, i, primes[i - 1], marker, enough))
    deviations = [node for node in nodes if not node["C_n_equals_P_n"]]
    ok = len(nodes) > 0 and not deviations
    system = {
        "P": PROTOCOL,
        "Owner": owner,
        "Rule": "all public repositories are sorted and encoded as C_n+n*i with C_n=P_n",
        "N": len(nodes),
        "Nodes": nodes,
        "Deviations": deviations,
        "H": 0 if ok else 1,
        "ZE": 1 if ok else 0,
        "Rb": "solved" if ok else "unsolved",
        "TM": "halt_accept" if ok else "halt_review",
        "SHA": 0,
        "ExternalFileExecution": 0,
        "RuntimeSource": "GitHub public repository metadata API",
        "RHProof": False,
        "Boundary": "Repo metadata marker encoding only; not source-body restoration and not RH proof.",
        "T": utc(),
    }
    system["SystemCRC32"] = format(zlib.crc32(canon(system).encode("utf-8")) & 0xFFFFFFFF, "08x")
    return system


def verify(system: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "has_nodes": system.get("N", 0) > 0,
        "markers_match_primes": not system.get("Deviations"),
        "no_sha": system.get("SHA") == 0,
        "no_external_execution": system.get("ExternalFileExecution") == 0,
        "honest_boundary": system.get("RHProof") is False,
    }
    ok = all(checks.values())
    return {
        "P": PROTOCOL,
        "Owner": system.get("Owner"),
        "N": system.get("N", 0),
        "TM": "halt_accept" if ok else "halt_review",
        "H": 0 if ok else 1,
        "ZE": 1 if ok else 0,
        "Rb": "solved" if ok else "unsolved",
        "DeviationCount": len(system.get("Deviations", [])),
        "SystemCRC32": system.get("SystemCRC32"),
        "checks": checks,
    }


def print_text(system: dict[str, Any]) -> None:
    print("RH All-Repos Marker Encoding")
    print("owner=%s repos=%s TM=%s" % (system["Owner"], system["N"], system["TM"]))
    print("H=%s ZE=%s Rb=%s deviations=%s" % (
        system["H"],
        system["ZE"],
        system["Rb"],
        len(system["Deviations"]),
    ))
    if system["Nodes"]:
        first = system["Nodes"][0]
        print("first=%s z=%s" % (first["r"], first["z_marker"]))
    print("RHProof=false ExternalFileExecution=0")


def main() -> int:
    parser = argparse.ArgumentParser(description="Encode all public repos as RH prime markers")
    parser.add_argument("command", nargs="?", default="observe", choices=["observe", "json", "verify"])
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--inject-index", type=int)
    parser.add_argument("--inject-c", type=int)
    args = parser.parse_args()
    system = build(args.owner, args.timeout, args.inject_index, args.inject_c)
    if args.command == "json":
        print(canon(system))
    elif args.command == "verify":
        print(canon(verify(system)))
    else:
        print_text(system)
    return 0 if system["H"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
