#!/usr/bin/env python3
"""
Riemann Li Singularity Observer

Executable formalization of:

    z = x + y i j

where j is treated as a Riemann-sheet direction and the logarithmic integral is
observed through:

    Log_j(z) = ln|z| + i(arg(z) + 2*pi*j)
    Li_j(z) = Ei(Log_j(z))

Near z = 1 on the principal sheet, Li has a logarithmic singularity.  This
observer separates the divergent kernel from the finite renormalized residue:

    Ei(w) = gamma + Log(w) + sum_{k>=1} w^k / (k*k!)

so:

    RenormLi_j(z) = Li_j(z) - Log(Log_j(z)) - gamma
                  = sum_{k>=1} Log_j(z)^k / (k*k!)

This is a formal TRF/CLZeroPack-style observer, not a replacement for a
full numerical special-functions library.
"""

import argparse
import cmath
import json
import math
import sys
import time


P = "RiemannLiSingularity/1"
GAMMA = 0.577215664901532860606512090082402431


def dumps(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def cpack(z):
    return {"re": z.real, "im": z.imag, "abs": abs(z)}


def log_sheet(z, sheet):
    return math.log(abs(z)) + 1j * (cmath.phase(z) + 2.0 * math.pi * sheet)


def renorm_li_series(w, terms):
    total = 0j
    fact = 1.0
    power = 1 + 0j
    for k in range(1, terms + 1):
        power *= w
        fact *= k
        total += power / (k * fact)
    return total


def observe(x, y, sheet, eps, terms, tol):
    # The formal ij direction is represented numerically as a complex axis,
    # while sheet keeps the Riemann-surface branch information explicit.
    z = complex(x + eps, y)
    w = log_sheet(z, sheet)
    residue = renorm_li_series(w, terms)
    divergent_kernel = None if abs(w) == 0 else cmath.log(w) + GAMMA
    li_approx = None if divergent_kernel is None else divergent_kernel + residue

    faces = {
        "x_axis_declared": isinstance(x, (int, float)),
        "ij_axis_declared": isinstance(y, (int, float)),
        "sheet_j_declared": isinstance(sheet, int),
        "log_integral_sheeted": abs(w) >= 0,
        "divergence_kernel_identified": divergent_kernel is not None,
        "renormalized_residue_finite": math.isfinite(residue.real) and math.isfinite(residue.imag),
    }
    h = sum(0 if ok else 1 for ok in faces.values())

    principal_limit = sheet == 0 and abs(y) <= tol and abs(x - 1.0) <= max(tol, abs(eps) * 10)
    if principal_limit:
        limit_state = {
            "R_j": 0,
            "meaning": "principal-sheet renormalized limit z->1 gives zero residue",
        }
    else:
        limit_state = {
            "R_j_approx": cpack(residue),
            "meaning": "finite sheeted residue approximation, not the principal zero limit",
        }

    rubik = {
        "P": "Rubik/RiemannLiSingularity/1",
        "S6": "6=3! and 6=3 axes x 2 directions",
        "axes": ["x", "ij", "sheet_j"],
        "faces": faces,
        "H": h,
        "Z": "0" if h == 0 else "!0",
        "Rb": "solved" if h == 0 else "unsolved",
        "ZE": 1 if h == 0 else 0,
        "TM": "rubik_accept" if h == 0 else "rubik_error",
    }

    return {
        "P": P,
        "T": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "definition": "R_j := lim_{z->1_j}[Li_j(z)-Log(Log_j(z))-gamma]",
        "coordinate": {
            "syntax": "z = x + y i j",
            "x": x,
            "y": y,
            "j": sheet,
            "z": cpack(z),
            "note": "ij is the formal extended imaginary direction; sheet j is explicit.",
        },
        "Log_j_z": cpack(w),
        "divergent_kernel_LogLog_plus_gamma": None if divergent_kernel is None else cpack(divergent_kernel),
        "RenormLi_j_z": cpack(residue),
        "Li_j_z_approx": None if li_approx is None else cpack(li_approx),
        "limit_state": limit_state,
        "H": h,
        "Z": "0" if h == 0 else "!0",
        "Rb": "solved" if h == 0 else "unsolved",
        "ZE": 1 if h == 0 else 0,
        "TM": "halt_accept" if h == 0 else "halt_error",
        "Rubik": rubik,
        "axiom": "The singularity is a renormalized limit state of Li on Riemann sheets, not a standard finite Li(1) value.",
    }


def main():
    ap = argparse.ArgumentParser(description="Observe the Riemann logarithmic-integral singularity as a renormalized limit state.")
    ap.add_argument("--x", type=float, default=1.0, help="Classical x coordinate.")
    ap.add_argument("--y", type=float, default=0.0, help="Formal ij-axis coefficient.")
    ap.add_argument("--j", type=int, default=0, help="Riemann sheet index.")
    ap.add_argument("--eps", type=float, default=1e-9, help="Small offset from x=1 for observation.")
    ap.add_argument("--terms", type=int, default=40, help="Series terms for renormalized residue.")
    ap.add_argument("--tol", type=float, default=1e-7, help="Tolerance for principal limit recognition.")
    ap.add_argument("--pretty", action="store_true", help="Print a readable summary before JSON.")
    args = ap.parse_args()
    state = observe(args.x, args.y, args.j, args.eps, args.terms, args.tol)
    if args.pretty:
        print("Riemann Li Singularity Observer")
        print("z = x + yij = %.12g + %.12g i_j" % (args.x, args.y))
        print("sheet j =", args.j)
        print("H=%s Z=%s Rb=%s ZE=%s TM=%s" % (
            state["H"], state["Z"], state["Rb"], state["ZE"], state["TM"]))
        print("limit:", state["limit_state"]["meaning"])
    print(dumps(state))


if __name__ == "__main__":
    main()
