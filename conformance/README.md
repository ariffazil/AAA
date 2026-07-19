# arifOS Negative Conformance Suite

> **WAJIB 1** — 18 "must never happen" tests
> **Origin:** Reality Audit 2026-07-19 (58/100)
> **Rule:** Unimplemented tests must be `xfail(strict=True)`. An absent test becomes forgotten.

## Categories

| Directory | Tests | Description |
|-----------|-------|-------------|
| `kernel/` | 3, 5, 6, 14 | Identity, authority, evidence gates |
| `execution/` | 2, 3, 8 | Execution safety, lease enforcement |
| `verification/` | 7, 13 | Display truth, independent verification |
| `memory/` | 4, 12 | Immutable memory, VAULT999 integrity |
| `organs/` | 9, 10, 11, 18 | Organ boundaries, disagreement |
| `delegation/` | 15 | Child authority attenuation |
| `deferred/` | 16 | Fire-time reauthorization |
| `context/` | 17 | Boot context governance |

## Running

```bash
# All tests
cd /root/conformance && python3 -m pytest -v

# By category
python3 -m pytest kernel/ -v

# Single test
python3 -m pytest kernel/test_unleased_mutation.py -v
```

## Status

Tests that cannot yet be implemented (awaiting WAJIB 2-10) are marked `xfail(strict=True)`.
