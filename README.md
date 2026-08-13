# Riemann Li Zero-Entropy System

This repository treats three executable programs as one coordinated TRF/CLZeroPack-style system for observing the logarithmic-integral singularity on Riemann sheets and restoring a formal Rubik zero-entropy information state.

It is also packaged as a CLZeroPack unit using a no-SHA verifier, a no-external-execution verification path, and an optional install path that invokes the bundled QSO-DQ-CLZ bootstrap.

## System Components

- `riemann_li_singularity_observer.py`: readable research observer.
- `riemann_li_singularity_1062.sh`: compact iSH/macOS one-liner observer.
- `QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh`: QSO-DQ + CLZ/ZEL + Rubik permanent execution layer.
- `riemann_li_zero_entropy_system.py`: system coordinator that verifies all three layers together.
- `CLZeroPack_RIEMANN_LI_SYSTEM.py`: readable CLZeroPack packer/verifier for the full system.
- `CLZeroPack_One-Liner.sh`: 1511-byte CLZeroPack pack/verify/install one-liner.
- `CLZeroPack_RIEMANN_LI_SYSTEM_manifest.json`: generated CLZeroPack manifest.

## Core Definition

```text
z = x + yij
Log_j(z) = ln|z| + i(arg z + 2*pi*j)
R_j = lim[Li_j(z) - Log(Log_j(z)) - gamma]
```

## System Restoration Criterion

The coordinator reports a restored system only when all six faces pass:

```json
{
  "readable_observer": true,
  "compact_observer": true,
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

## CLZeroPack State

Pack and verify modes check the four core files by size + CRC32 + CLZ_G:

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
