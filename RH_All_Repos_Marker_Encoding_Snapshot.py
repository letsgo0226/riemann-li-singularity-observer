#!/usr/bin/env python3
"""Offline RH all-repos marker snapshot.

Embeds a 2026-08-16 snapshot of 105 letsgo0226 public repository names.
No network, no SHA, no external payload execution, and no RH proof claim.
"""
import argparse, base64, json, math, time, zlib

P = "CLZeroPack/RHAllReposMarkerEncoding/Snapshot/1"
OWNER = "letsgo0226"
SNAPSHOT_DATE = "2026-08-16"
B = "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"

def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
def repos(): return json.loads(zlib.decompress(base64.b64decode(B)).decode())
def ip(x): return x > 1 and all(x % d for d in range(2, int(math.isqrt(x)) + 1))
def primes(n):
    p=[]; x=2
    while len(p)<n:
        if ip(x): p.append(x)
        x += 1
    return p

def build(inj=0, ic=0):
    r = repos(); ps = primes(len(r)); nodes=[]; dev=[]
    for i, name in enumerate(r, 1):
        p = ps[i-1]; c = ic if inj == i and ic else p; ok = c == p
        node = {"r": name, "n": i, "P_n": p, "C_n": c, "z_marker": f"{c}+{i}i", "H": 0 if ok else 1, "ZE": 1 if ok else 0}
        nodes.append(node)
        if not ok: dev.append(node)
    ok = bool(nodes) and not dev
    o = {"P": P, "Owner": OWNER, "SnapshotDate": SNAPSHOT_DATE, "SnapshotStatic": True, "NetworkRequired": 0, "N": len(nodes), "Nodes": nodes, "DeviationCount": len(dev), "Deviations": dev, "H": 0 if ok else 1, "ZE": 1 if ok else 0, "Rb": "solved" if ok else "unsolved", "TM": "halt_accept" if ok else "halt_review", "SHA": 0, "ExternalFileExecution": 0, "RHProof": False, "Boundary": "Offline snapshot marker encoding only; not current GitHub state and not source-body restoration.", "T": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    o["SnapshotCRC32"] = format(zlib.crc32(canon(r).encode()) & 0xffffffff, "08x")
    o["SystemCRC32"] = format(zlib.crc32(canon(o).encode()) & 0xffffffff, "08x")
    return o

def verify(o):
    c = {"snapshot_count": o["N"] == 105, "markers_match_primes": o["DeviationCount"] == 0, "offline": o["NetworkRequired"] == 0, "no_sha": o["SHA"] == 0, "no_external_execution": o["ExternalFileExecution"] == 0, "honest_boundary": o["RHProof"] is False}
    ok = all(c.values())
    return {"P": P, "Owner": OWNER, "SnapshotDate": SNAPSHOT_DATE, "N": o["N"], "TM": "halt_accept" if ok else "halt_review", "H": 0 if ok else 1, "ZE": 1 if ok else 0, "Rb": "solved" if ok else "unsolved", "DeviationCount": o["DeviationCount"], "SnapshotCRC32": o["SnapshotCRC32"], "checks": c}

def main():
    a = argparse.ArgumentParser(); a.add_argument("command", nargs="?", default="observe", choices=["observe", "json", "verify"]); a.add_argument("--inject-index", type=int, default=0); a.add_argument("--inject-c", type=int, default=0); x = a.parse_args(); o = build(x.inject_index, x.inject_c)
    if x.command == "json": print(canon(o))
    elif x.command == "verify": print(canon(verify(o)))
    else:
        print("RH All-Repos Marker Snapshot")
        print("owner=%s snapshot=%s repos=%s TM=%s" % (OWNER, SNAPSHOT_DATE, o["N"], o["TM"]))
        print("H=%s ZE=%s Rb=%s deviations=%s NetworkRequired=0" % (o["H"], o["ZE"], o["Rb"], o["DeviationCount"]))
        print("SnapshotCRC32=%s RHProof=false" % o["SnapshotCRC32"])
    return 0 if o["H"] == 0 else 1
if __name__ == "__main__": raise SystemExit(main())
