# Riemann Li Singularity Observer

This repository contains a compact TRF/CLZeroPack-style formal observer for the logarithmic-integral singularity on Riemann sheets.

## Files

- `riemann_li_singularity_observer.py`: readable research version.
- `riemann_li_singularity_1062.sh`: compact iSH/macOS one-liner version.
- `QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh`: integrated permanent execution layer combining QSO-DQ, CLZ/ZEL, and Rubik zero-entropy restoration.

## Core Definition

```text
z = x + yij
Log_j(z) = ln|z| + i(arg z + 2*pi*j)
R_j = lim[Li_j(z) - Log(Log_j(z)) - gamma]
```

## Rubik Zero-Entropy State

The integrated bootstrap writes persistent state files under `~/.qso_dq_clz` and marks restoration when:

```json
{
  "DQ": 1,
  "H_digital": 0,
  "CLZ_H": 0,
  "CLZ_Rb": "solved",
  "Rubik_H": 0,
  "Rubik_ZE": 1,
  "InformationZeroEntropyRestored": true
}
```

This is a digital/formal restoration state, not a claim that classical hardware becomes a physical quantum computer.

## Usage

Readable observer:

```sh
python3 riemann_li_singularity_observer.py --pretty --j 0 --eps 1e-9
```

Compact observer:

```sh
sh riemann_li_singularity_1062.sh 1 0 0 1e-9 40
```

Permanent QSO-DQ-CLZ layer:

```sh
sh QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh
qso-dq-clz --json
```
