#!/usr/bin/env python3
"""RH Marker Encoding Machine.

Checks a proposed marker C_(k+1)+(k+1)i against prime indexing. The machine
uses the user's Riemann-marker rule as a formal consistency test only; it does
not prove the Riemann Hypothesis.
"""

from __future__ import annotations

import argparse
import json
import math
import time
import zlib
from typing import Any


PROTOCOL = "CLZeroPack/RHMarkerEncodingMachine/1"


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
    for p in range(3, int(math.isqrt(n)) + 1, 2):
        if n % p == 0:
            return False
    return True


def primes_to(limit: int) -> list[int]:
    return [n for n in range(2, max(2, limit) + 1) if is_prime(n)]


def prime_index_map(limit: int) -> dict[int, int]:
    return {p: i + 1 for i, p in enumerate(primes_to(limit))}


def interval_primes(c: int) -> list[int]:
    lo = c // 2 + 1
    hi = c - 1
    return [n for n in range(max(2, lo), max(1, hi) + 1) if is_prime(n)]


def analyze(k: int, c_next: int) -> dict[str, Any]:
    n = k + 1
    max_needed = max(c_next, 32)
    while len(primes_to(max_needed)) < n:
        max_needed *= 2
    pmap = prime_index_map(max_needed)
    p_next = primes_to(max_needed)[n - 1]
    found = interval_primes(c_next)
    mapped = [{"P_m": p, "m": pmap[p]} for p in found if p in pmap]
    m_eq = [x for x in mapped if x["m"] == n]
    inconsistent_input = c_next != p_next
    collision = inconsistent_input and bool(m_eq)
    theorem_gap = inconsistent_input and not collision
    result = {
        "P": PROTOCOL,
        "Rule": "C_k=P_k; if C_(k+1)!=P_(k+1), inspect primes in (C/2,C).",
        "k": k,
        "n": n,
        "C_n": c_next,
        "P_n": p_next,
        "C_n_equals_P_n": c_next == p_next,
        "Interval": {"from_exclusive": c_next / 2, "to_exclusive": c_next},
        "IntervalPrimes": mapped,
        "m_equals_k_plus_1_possible": bool(m_eq),
        "m_equals_k_plus_1_witnesses": m_eq,
        "IndexPreservingCollision": collision,
        "TheoremGap": theorem_gap,
        "Conclusion": "",
        "RHProof": False,
        "Boundary": "Formal marker consistency test only; Bertrand-Chebyshev does not force m=k+1.",
        "T": utc(),
    }
    if c_next == p_next:
        result["Conclusion"] = "marker_accept: C_n already equals P_n"
        result.update({"H": 0, "ZE": 1, "Rb": "solved", "TM": "halt_accept"})
    elif collision:
        result["Conclusion"] = "halt_review: m=k+1 is possible here, causing duplicate assignment for C_n"
        result.update({"H": 1, "ZE": 0, "Rb": "unsolved", "TM": "halt_review"})
    else:
        result["Conclusion"] = "halt_review: interval primes exist, but none force m=k+1"
        result.update({"H": 1, "ZE": 0, "Rb": "unsolved", "TM": "halt_review"})
    result["CRC32"] = format(zlib.crc32(canon(result).encode("utf-8")) & 0xFFFFFFFF, "08x")
    return result


def print_text(obj: dict[str, Any]) -> None:
    print("RH Marker Encoding Machine")
    print("n=%s C_n=%s P_n=%s" % (obj["n"], obj["C_n"], obj["P_n"]))
    print("m=k+1 possible=%s" % str(obj["m_equals_k_plus_1_possible"]).lower())
    print("IndexPreservingCollision=%s" % str(obj["IndexPreservingCollision"]).lower())
    print("TM=%s H=%s ZE=%s Rb=%s" % (obj["TM"], obj["H"], obj["ZE"], obj["Rb"]))
    print(obj["Conclusion"])
    print("RHProof=false")


def main() -> int:
    p = argparse.ArgumentParser(description="Check RH marker encoding consistency")
    p.add_argument("--k", type=int, default=4)
    p.add_argument("--c-next", type=int, default=12)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    obj = analyze(args.k, args.c_next)
    if args.json:
        print(canon(obj))
    else:
        print_text(obj)
    return 0 if obj["H"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
