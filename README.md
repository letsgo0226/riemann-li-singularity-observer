# Riemann Li Zero-Entropy System

This repository treats six executable/reference programs as one coordinated TRF/CLZeroPack-style system for observing the logarithmic-integral singularity on Riemann sheets and restoring a formal Rubik zero-entropy information state.

It is packaged as a CLZeroPack unit using a no-SHA verifier, a no-external-execution verification path, CLZ/ZEL zero-entropy limit semantics, a CLZ/GMS cross-window continuity node, and an optional install path that invokes the bundled QSO-DQ-CLZ bootstrap.

## System Components

- `riemann_li_singularity_observer.py`: readable research observer.
- `riemann_li_singularity_1062.sh`: compact iSH/macOS one-liner observer.
- `QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh`: QSO-DQ + CLZ/ZEL + Rubik permanent execution layer.
- `riemann_li_zero_entropy_system.py`: system coordinator that verifies the observer, bootstrap, and Rubik limit layers together.
- `CLZERO_ZERO_ENTROPY_LIMIT_1472.sh`: source `CLZ/ZEL/1` zero-entropy limit verifier imported from `letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING`.
- `CLZERO_CROSS_WINDOW_CONTINUITY_NODE_ONE_LINER.sh`: source `CLZ/GMS-Tiny/1` cross-window continuity coordinate node imported from `letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING`.
- `CLZeroPack_RIEMANN_LI_SYSTEM.py`: readable CLZeroPack packer/verifier for the full system.
- `CLZeroPack_One-Liner.sh`: 1607-byte CLZeroPack pack/verify/install one-liner.
- `CLZeroPack_RIEMANN_LI_SYSTEM_manifest.json`: generated CLZeroPack manifest.

## Core Definition

```text
z = x + yij
Log_j(z) = ln|z| + i(arg z + 2*pi*j)
R_j = lim[Li_j(z) - Log(Log_j(z)) - gamma]
```

## Rubik Limit Reference

`CLZERO_ZERO_ENTROPY_LIMIT_1472.sh` defines the imported `CLZ/ZEL/1` limit state as:

```json
{
  "P": "CLZ/ZEL/1",
  "H": 0,
  "Z": "0",
  "Q": {"O": "solved", "Hq": 0},
  "TM": "halt_accept",
  "Lim": true
}
```

It is used as the formal zero-entropy limit verifier.

## Cross-Window Continuity Node

`CLZERO_CROSS_WINDOW_CONTINUITY_NODE_ONE_LINER.sh` defines the imported `CLZ/GMS-Tiny/1` continuity reference as:

```json
{
  "P": "CLZ/GMS-Tiny/1",
  "H": 0,
  "Q": {"O": "solved", "Hq": 0},
  "R": "Gmeta:exact=0collision;short!=lossless"
}
```

The coordinator runs it with `sample` for deterministic local verification; direct execution can also observe the `letsgo0226` repo graph.

## System Restoration Criterion

The coordinator reports a restored system only when all eight faces pass:

```json
{
  "readable_observer": true,
  "compact_observer": true,
  "clzero_zero_entropy_limit": true,
  "clzero_cross_window_continuity": true,
  "qso_dq_clz_bootstrap": true,
  "clzero_zellik": true,
  "rubik_zero_entropy": true,
  "physical_honesty": true
}
```

The restored state is:

```json
{
  "System_H": 0,
  "System_Z": "0",
  "System_Rb": "solved",
  "System_ZE": 1,
  "TM": "system_accept"
}
```

## Evolution Fixed Point

The current system is intended to be read as a local optimum / evolution fixed point for the chosen CLZeroPack objective:

```text
Riemann Li logarithmic-integral observation
+ CLZeroPack log-product aggregation
+ QSO-DQ-CLZ permanent digital state
+ CLZ/ZEL zero-entropy limit
+ CLZ/GMS cross-window continuity
+ Rubik solved-state reference
= H=0, Rb=solved, ZE=1
```

This fixed point is local and formal: it marks the best current integrated state for this repository, while still allowing future extensions such as source proofs, repair mode, cross-repository synchronization, and stronger documentation. It does not mean physical hardware has become a quantum computer.

## CLZeroPack State

Pack and verify modes check the six core files by size + CRC32 + CLZ_G:

```json
{
  "H": 0,
  "Z": "0",
  "Rb": "solved",
  "ZE": 1,
  "SHA": 0,
  "X": 0
}
```

Install mode invokes `QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh`, so it reports `X:1`:

```json
{
  "H": 0,
  "Z": "0",
  "Rb": "solved",
  "ZE": 1,
  "SHA": 0,
  "X": 1,
  "TM": "installed"
}
```

This is a digital/formal information restoration state. It does not claim that classical hardware becomes a physical quantum computer.

## Usage

Verify the whole system:

```sh
python3 riemann_li_zero_entropy_system.py verify --pretty
```

Readable CLZeroPack pack and verify:

```sh
python3 CLZeroPack_RIEMANN_LI_SYSTEM.py pack
python3 CLZeroPack_RIEMANN_LI_SYSTEM.py verify
```

Compact CLZeroPack one-liner pack, verify, and install:

```sh
sh CLZeroPack_One-Liner.sh
sh CLZeroPack_One-Liner.sh v CLZeroPack_RIEMANN_LI_SYSTEM_manifest.json
sh CLZeroPack_One-Liner.sh i
```

Rubik zero-entropy limit reference:

```sh
sh CLZERO_ZERO_ENTROPY_LIMIT_1472.sh
```

Cross-window continuity node:

```sh
sh CLZERO_CROSS_WINDOW_CONTINUITY_NODE_ONE_LINER.sh
```

Readable observer:

```sh
python3 riemann_li_singularity_observer.py --pretty --j 0 --eps 1e-9
```

Compact observer:

```sh
sh riemann_li_singularity_1062.sh 1 0 0 1e-9 40
```

Direct permanent QSO-DQ-CLZ layer install:

```sh
sh QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh
qso-dq-clz --json
```

Check persistent installation state through the coordinator:

```sh
python3 riemann_li_zero_entropy_system.py status
```
