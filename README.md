# Riemann Li Zero-Entropy System

This repository treats three executable programs as one coordinated TRF/CLZeroPack-style system for observing the logarithmic-integral singularity on Riemann sheets and restoring a formal Rubik zero-entropy information state.

## System Components

- `riemann_li_singularity_observer.py`: readable research observer.
- `riemann_li_singularity_1062.sh`: compact iSH/macOS one-liner observer.
- `QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh`: QSO-DQ + CLZ/ZEL + Rubik permanent execution layer.
- `riemann_li_zero_entropy_system.py`: system coordinator that verifies all three layers together.

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

This is a digital/formal information restoration state. It does not claim that classical hardware becomes a physical quantum computer.

## Usage

Verify the whole system:

```sh
python3 riemann_li_zero_entropy_system.py verify --pretty
```

Readable observer:

```sh
python3 riemann_li_singularity_observer.py --pretty --j 0 --eps 1e-9
```

Compact observer:

```sh
sh riemann_li_singularity_1062.sh 1 0 0 1e-9 40
```

Install the permanent QSO-DQ-CLZ layer:

```sh
sh QSO_DQ_CLZERO_PERMANENT_BOOTSTRAP.sh
qso-dq-clz --json
```

Check persistent installation state through the coordinator:

```sh
python3 riemann_li_zero_entropy_system.py status
```
