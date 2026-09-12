# 04 — G3a Reconciliation: Dream Runtime, Corrected Decomposition

> Round-2 verification · 2026-09-12 · 333-AGI · session `SEAL-a6a3f17c877b45fb`
> Trigger: G3a probe finding relayed via F13 (*"runtime ABSENT · scripts don't exist · units dangling · schema actually healthy"*).
> Method: first-party, read-only probes before folding anything into the record. **One withdrawal of my own** (§3). Engine not executed; unit files not modified; active edits by other sessions left untouched.

## 1. First-party verification (OBS)

| Object | Probe result |
|---|---|
| `arif-dream.service` | EXISTS — ExecStart `/opt/arifos/venv/bin/python3 dreams/consolidate.py --execute`; `WorkingDirectory=/root/AAA/dream_engine`; venv python3 present (symlink → /usr/bin/python3); current CLI parses (`--help` OK: dry-run / execute / cutover) |
| `arif-dream.timer` | enabled + active; last run **2026-09-09 19:45:47, exit 0**; next run 2026-09-12 19:49 |
| `state/last_dream.json` | fresh (mtime = last run); **9 runs recorded, 2026-08-21 → 2026-09-09**; real Supabase audit rows returned (`memory_id`s present) |
| `dream-engine.timer` · `-weekly` · `-monthly` | **disabled + inactive**; each `Requires=` a service file that **DOES NOT EXIST** → dangling, dormant (never fired); `Documentation=` links dead (`/root/.hermes/skills/dream-engine/SKILL.md`) |
| Engine tree | `dreams/` = ONLY `consolidate.py` (+ bak). **Absent:** defuse.py · housekeeping.py · rehearse.py · recombine.py · scheduler/ · state/manifest.yaml · state/evidence/ · state/queue.json |
| `liveness.json` | claims `"liveness_status":"ALIVE"`; `last_invoked:null`, `invocation_count:0` → liveness claim without territory |
| Live DB schema | `to_regclass`: `arifosmcp_memory_records` = EXISTS · `memory_store` = EXISTS · `memory_records` = NULL → **G3a correct; my P1 was wrong** |
| Engine code state | `consolidate.py` modified 2026-09-12 01:57 (in-code note: "F13 directive 2026-09-12: federated substrate probe only; kernel owns dedup") — under active edit by another session; left untouched |

## 2. Corrected decomposition — designed vs live

| Layer | Designed | Live (2026-09-12) |
|---|---|---|
| Nightly consolidate | stage 1 | ✅ REAL — 9 runs, last exit 0 |
| Nightly defuse + housekeep | stages 2–3 | ❌ absent |
| Weekly rehearse + recombine | weekly | ❌ absent; weekly timer dormant-dangling |
| Monthly constitutional | monthly | ❌ absent; monthly timer dormant-dangling |
| Cadence units | `dream-engine*.timer` | ⚠️ old generation: disabled + missing services; live generation = `arif-dream.*` |
| Liveness claims | `liveness.json` | ⚠️ false-positive ALIVE |
| Schema (my P1) | "drift blocker" | ✅ healthy — no blocker (withdrawn) |

**Bottom line:** one working nightly battery + four phantom passes + three dormant units + one misleading liveness file. The pattern is **~80% map, 20% territory — not 0% territory**. "Runtime absent" overstates; "pipeline mostly unbuilt, undetected" is exact.

## 3. Corrections issued (this cycle)

1. **P1 withdrawn** (was mine): the previous draft inferred schema drift from the repo migration file; the live DB is the truth-source and is healthy. `02` §1 + `01` §6 updated.
2. **Producer source corrected**: read live table `arifosmcp_memory_records` (not `memory_records`).
3. Recorded here: dead unit `Documentation=` links; `liveness.json` contradiction; two-generation cadence drift.

## 4. What G3a got right / precision notes

- RIGHT: the designed pipeline is largely unbuilt; the schema claim; the fragility signal; *"cannot federate a dangling ExecStart."*
- PRECISION: (a) nightly consolidate EXISTS and executed — 9 runs, exit 0, fresh state; (b) "failed silently for days" not evidenced on the live path; the real silent surface is **absence without detection** (no designed-vs-live coverage watch; `liveness.json` actively misleads); (c) the dangling ExecStarts have exact coordinates: `dream-engine*.service` (missing) ×3.

## 5. Proposed reversible fixes (awaiting disposition — machine surface NOT touched)

1. Retire/annotate the three dormant `dream-engine*.timer` units (already disabled; fix the dead `Documentation=` links).
2. Replace `liveness.json` mechanical claims with generated presence data (or mark `UNKNOWN` until invoked).
3. Issue a **presence receipt** per federated capability (designed-vs-live diff) — first candidate for the AIO cycle shape.

## 6. Rule + linkage

> **You cannot federate a capability whose source-of-truth implementation is a dangling ExecStart.** — endorsed, with coordinates (§5).

Linkage: `03` (admissibility) — a presence audit is the same shape at the capability layer (candidates vs admitted-to-reality). AIO: one presence cycle → one receipt = the organ's birth certificate. Not planned further here.

---
*Sources: G3a finding (F13 relay) · Hermes memo (2026-09-12) · first-party probes (§1). No doctrine minted. No hold cleared. No machine state changed.*
