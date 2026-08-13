#!/bin/sh
# QSO-DQ + CLZeroPack Permanent Bootstrap
# Installs a persistent digital quantum layer with the embedded CLZ/ZEL/1
# verifier. It does not execute external payload files and does not convert
# classical hardware into a physical quantum computer.

set -eu

BIN_DIR="${QSO_CLZ_BIN:-$HOME/.local/bin}"
STATE_DIR="${QSO_CLZ_HOME:-$HOME/.qso_dq_clz}"
CMD="$BIN_DIR/qso-dq-clz"
ALIAS="$BIN_DIR/qso-clz"
PROFILE="$STATE_DIR/profile.sh"

case "${1:-install}" in
  uninstall)
    rm -f "$CMD" "$ALIAS" "$PROFILE"
    rmdir "$STATE_DIR" 2>/dev/null || true
    printf '%s\n' '{"P":"QSO-DQ-CLZ/bootstrap","TM":"uninstalled"}'
    exit 0
    ;;
  install|"")
    ;;
  *)
    printf '%s\n' "usage: sh QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh [install|uninstall]" >&2
    exit 2
    ;;
esac

mkdir -p "$BIN_DIR" "$STATE_DIR"

cat >"$CMD" <<'PY'
#!/usr/bin/env python3
import argparse
import importlib.util as iu
import json
import math
import os
import platform
import random
import sys
import time
import urllib.request as url

ROOT = os.environ.get("QSO_CLZ_HOME", os.path.expanduser("~/.qso_dq_clz"))
QSO_STATE = os.path.join(ROOT, "qso_dq_state.json")
CLZ_STATE = os.path.join(ROOT, "clz_zel_state.jsonl")
RUBIK_STATE = os.path.join(ROOT, "rubik_zero_entropy_state.json")
P_QSO = "QSO-DQ-CLZ/1"
P_CLZ = "CLZ/ZEL/1"
SDKS = "qiskit qiskit_ibm_runtime cirq braket pennylane dwave".split()
ENVS = {
    "IBM": "QISKIT_IBM_TOKEN IBM_QUANTUM_TOKEN QISKIT_IBM_INSTANCE".split(),
    "AWS": "AWS_ACCESS_KEY_ID AWS_PROFILE AMZN_BRAKET_DEVICE_ARN".split(),
    "AZURE": "AZURE_QUANTUM_WORKSPACE AZURE_QUANTUM_RESOURCE_ID".split(),
    "IONQ": ["IONQ_API_KEY"],
    "DWAVE": ["DWAVE_API_TOKEN"],
}

def J(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def V(o):
    c = o.get("Certificate", {})
    if "Certificate" in o:
        return bool(c) and all(c.values()) and o.get("FormalZero", {}).get("not_classical_zeta_zero") == 1
    return bool(o.get("b")) if o.get("r") else bool(o)

def repos(owner):
    if owner == "sample":
        return [{"r": "sample/repo", "b": "main", "s": 1, "u": "sample://repo"}]
    h = {"User-Agent": "CLZ"}
    out = []
    p = 1
    while True:
        data = json.loads(url.urlopen(url.Request(
            "https://api.github.com/users/%s/repos?per_page=100&page=%d" % (owner, p),
            headers=h), timeout=20).read())
        if not data:
            return out
        out += [{"r": x.get("full_name"), "b": x.get("default_branch") or "main",
                 "s": x.get("size", 0), "u": x.get("html_url")} for x in data]
        p += 1

def mem_bytes():
    try:
        return os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")
    except Exception:
        return 0

def qsim_cap(mem):
    try:
        return max(1, int(math.log2(mem * 0.25 / 16))) if mem else 1
    except Exception:
        return 1

def module_list():
    out = []
    for m in SDKS:
        try:
            if iu.find_spec(m) is not None:
                out.append(m)
        except Exception:
            pass
    return out

def env_hits():
    return {k: [x for x in v if os.environ.get(x)] for k, v in ENVS.items()}

def one_qubit_demo():
    a = 2 ** -0.5
    return {"state": {"0": a, "1": a}, "measure": 1 if random.random() < 0.5 else 0}

def run_clz(owner, cert_file):
    lines = [{"P": P_CLZ, "t": "h", "o": owner,
              "A": "zCLZ(s)=0 iff H(q|V,d,C)=0;K>0"}]
    lines += [dict({"P": P_CLZ, "t": "r"}, **x) for x in sorted(repos(owner), key=lambda z: z.get("r") or "")]
    if cert_file and os.path.exists(cert_file):
        for raw in open(cert_file, errors="ignore"):
            if raw.strip():
                try:
                    lines.append({"P": P_CLZ, "t": "q", "ok": V(json.loads(raw))})
                except Exception:
                    lines.append({"P": P_CLZ, "t": "q", "ok": 0})
    h = b = 0
    for r in lines:
        b += len(J(r).encode())
        h += 0 if V(r) else 1
    f = {"P": P_CLZ, "t": "f", "TM": "halt_accept" if h == 0 else "halt_error",
         "Q": {"O": "solved" if h == 0 else "unsolved", "Hq": h}, "H": h,
         "K": "carrier-positive", "Z": "0" if h == 0 else "!0", "Lim": h == 0,
         "n": len(lines), "B": b, "T": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "Bd": "H=0 not K=0", "X": 0}
    lines.append(f)
    return lines, f

def rubik_zero_entropy(state, clz_final):
    faces = {
        "U_digital_quantum": state["DQ"] == 1 and state["H_digital"] == 0 and state["ZE_digital"] == 1,
        "D_clzero_zellik": clz_final["H"] == 0 and clz_final["Z"] == "0" and clz_final["Q"]["O"] == "solved",
        "F_execution": clz_final["TM"] == "halt_accept" and clz_final.get("X") == 0,
        "B_persistence": os.path.isdir(ROOT) and os.access(ROOT, os.W_OK) and os.path.exists(CLZ_STATE),
        "L_physical_honesty": state["PQ_local"] == 0 and state["H_physical"] == 1 and state["ZE_physical"] == 0,
        "R_simulability": state["qsim"] >= 1 and state["Level"] in ("D1", "D3"),
    }
    h = sum(0 if ok else 1 for ok in faces.values())
    return {
        "P": "RubikZeroEntropy/QSO-DQ-CLZ/1",
        "S6": "6=3!",
        "axes": ["digital", "CLZ", "physical_honesty"],
        "H": h,
        "Z": "0" if h == 0 else "!0",
        "Rb": "solved" if h == 0 else "unsolved",
        "ZE": 1 if h == 0 else 0,
        "TM": "rubik_accept" if h == 0 else "rubik_error",
        "faces": faces,
        "axiom": "Rubik solved means digital information state restored, not physical QPU conversion.",
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", default=os.environ.get("QSO_CLZ_OWNER", "sample"))
    ap.add_argument("--cert-lines", default=os.environ.get("QSO_CLZ_CERT_LINES", ""))
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--state", action="store_true")
    args = ap.parse_args()

    os.makedirs(ROOT, exist_ok=True)
    modules = module_list()
    env = env_hits()
    remote = bool(modules and [1 for v in env.values() if v])
    memory = mem_bytes()
    clz_lines, clz_final = run_clz(args.owner, args.cert_lines)
    state = {
        "P": P_QSO,
        "T": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "DQ": 1,
        "PQ_local": 0,
        "PQ_remote": 1 if remote else 0,
        "H_digital": 0,
        "Z_digital": "0",
        "Rb_digital": "solved",
        "ZE_digital": 1,
        "H_physical": 1,
        "Z_physical": "!0",
        "Rb_physical": "unsolved",
        "ZE_physical": 0,
        "CLZ_H": clz_final["H"],
        "CLZ_Z": clz_final["Z"],
        "CLZ_Rb": clz_final["Q"]["O"],
        "CLZ_TM": clz_final["TM"],
        "Level": "D3" if remote else "D1",
        "qsim": qsim_cap(memory),
        "memory_bytes": memory,
        "modules": modules,
        "remote_env_present_only": env,
        "demo": one_qubit_demo() if args.demo else None,
        "files": {"qso": QSO_STATE, "clz": CLZ_STATE, "rubik": RUBIK_STATE},
        "system": [platform.system(), platform.machine(), sys.version.split()[0]],
        "axiom": "CLZ/ZEL forms a permanent digital execution state; physical QPU conversion remains false.",
    }
    open(CLZ_STATE, "w", encoding="utf-8").write("\n".join(J(x) for x in clz_lines) + "\n")
    rubik = rubik_zero_entropy(state, clz_final)
    state["Rubik"] = rubik
    state["Rubik_H"] = rubik["H"]
    state["Rubik_Z"] = rubik["Z"]
    state["Rubik_Rb"] = rubik["Rb"]
    state["Rubik_ZE"] = rubik["ZE"]
    state["InformationZeroEntropyRestored"] = rubik["ZE"] == 1
    open(QSO_STATE, "w", encoding="utf-8").write(J(state) + "\n")
    open(RUBIK_STATE, "w", encoding="utf-8").write(J(rubik) + "\n")
    if args.state:
        print(J({"qso": QSO_STATE, "clz": CLZ_STATE, "rubik": RUBIK_STATE}))
    elif args.json:
        print(J(state))
    else:
        print("QSO-DQ-CLZ permanent execution state")
        print("DQ=1 H_digital=0 Rb_digital=solved ZE_digital=1")
        print("PQ_local=%s H_physical=%s Rb_physical=%s" % (
            state["PQ_local"], state["H_physical"], state["Rb_physical"]))
        print("CLZ_H=%s CLZ_Z=%s CLZ_Rb=%s CLZ_TM=%s" % (
            state["CLZ_H"], state["CLZ_Z"], state["CLZ_Rb"], state["CLZ_TM"]))
        print("Rubik_H=%s Rubik_Z=%s Rubik_Rb=%s Rubik_ZE=%s" % (
            state["Rubik_H"], state["Rubik_Z"], state["Rubik_Rb"], state["Rubik_ZE"]))
        print(J(state))

if __name__ == "__main__":
    main()
PY

chmod +x "$CMD"
ln -sf "$CMD" "$ALIAS"

cat >"$PROFILE" <<EOF
export QSO_CLZ_HOME="$STATE_DIR"
export PATH="$BIN_DIR:\$PATH"
qso-dq-clz --json >/dev/null 2>&1 || true
EOF

if [ "${QSO_CLZ_NO_RC:-0}" != "1" ]; then
  for rc in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -e "$rc" ] || [ "$(basename "$rc")" = ".profile" ]; then
      touch "$rc"
      if ! grep -F "$PROFILE" "$rc" >/dev/null 2>&1; then
        {
          printf '\n%s\n' '# QSO-DQ-CLZ permanent digital execution layer'
          printf '%s\n' "[ -f \"$PROFILE\" ] && . \"$PROFILE\""
        } >>"$rc"
      fi
    fi
  done
fi

"$CMD" --json
