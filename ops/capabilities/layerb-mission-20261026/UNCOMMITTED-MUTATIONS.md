# UNCOMMITTED-MUTATIONS — pointer for the 3 uncommitted source mutations

Mission `LAYER_B_DISCOVERY_CLOSURE_AND_FED_CALIBRATION` · 2026-10-26 · trace `trc-layerb-mission-20261026`
Why this file exists: the 888 judge (verdict HOLD, partial-seal scope) flagged that uncommitted
working-tree changes are a drift risk — any `git checkout` silently destroys them and no rollout
record exists. This pointer makes them discoverable. Full detail: `ROLLBACK.md` in this directory.

Status at write time: **all three uncommitted, none deployed.**

| id | repo | file | delta | commit recommendation |
|----|------|------|-------|-----------------------|
| M1 | /root/AAA | federation/organs.yaml | +16/−0 (mcp_port + interfaces for fed, geox, wealth, well; every value observed live) | **committable** — pure additive SOT completion; values measured, vocabulary copied from `components[id=arifos]` |
| M2 | /root/arif-fazil.com | sites/arif-fazil.com/public/.well-known/capabilities.json | +1/−1 (observatory_snapshot protocol mcp → http) | **awaits F13** — the file is a public-surface source; the live copy still says `mcp`, so committing the source without deploying changes nothing public, but deploy itself is the F13 call |
| M3 | /root/AAA | ops/capabilities/compile_machine_contract.py | v1.0 → v1.1 | **committable with warning** — commit message must state: v1.1 fixes defect C1 (response_schema reported 0/258; true value 138/258). Reverting re-introduces the false zero. |

Rollback: `ROLLBACK.md` steps A (M1), B (M2), C (M3). Pre-patch blobs:
M1 `0fd38b7a939a65d303e00fe24d6574b26a40ea23` · M2 `4f457d7eddd50c89a5df68945002ef772a4bc6e7` ·
M3 v1.0 `ea1bd293fcf82ab3c64f1681395cd06c429bf675aeecea9213afe0124ec853b8`.

Git-lane note: plain `git commit` is fail-closed in these repos; use
`/root/scripts/git-lane <lane> -C <repo> commit -m "..."`.
