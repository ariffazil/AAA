# 8 ≠ 9 Invariant — Session Forensics (2026-08-08)

The dialogue that produced §11 of `EUREKA_SIX_PLANE_EXECUTION_LOOP.md`.

## The paradox that wasn't

Initial framing was: "kernel verbs (8) ≠ cognitive atlas (9) — paradox, mismatch, gap?" The session evolved it to: **8 and 9 are different dimensions. The mismatch is constitutional, not a flaw.**

| Axis | Count | Invariant level |
|---|---|---|
| Kernel verbs | 8 | Constitutional machinery (rate-limiting for governance) |
| Cognitive atlas | 9 | Intelligence genome (functions without which complete intelligence is impossible) |
| W-vector | 9 floats | Mission-level expression profile |

**6 atlas functions map 1:1 to verbs. 3 don't (111/222/666). 2 verbs are substrate primitives (init/memory). 1 is partial (555).**

## Resolution statement (canonized)

> The kernel is the CONSTITUTIONAL MINIMUM — the verbs without which governed intelligence is impossible.
> The atlas is the COGNITIVE MAXIMUM — the functions without which complete intelligence is impossible.
> They converge at 6 points. They diverge at 5 (3 genome-only, 2 kernel-only).
> The W-vector bridges them per mission.

## Promotion criterion (the gate)

Question: **"Does compressing this function into another verb cause constitutional harm?"**

| Compression | Harm | Verdict | Promotion gate |
|---|---|---|---|
| 222 Architect → `arif_think(mode=plan)` | Minimal — shared substrate | ACCEPT | — |
| 555 Verifier → `arif_memory` + `arif_think` | Moderate — gaps across two verbs | WATCH | `arif_verify` after audit stable |
| **666 Auditor → `arif_judge`** | **Yes — Gödel lock at kernel level** | **PROMOTE-CANDIDATE** | 5+ missions OR FRAME/A-auditor gap leaks OR concrete F1/F11/F13 breach |
| 111 Explorer → `arif_observe` | Minimal — observation with intent delta | ACCEPT for now | domain tool, not kernel verb (likely never `arif_explore`) |

## The Gödel lock (single dangerous compression)

When `arif_judge` both rules on actions AND audits its own rulings, the loop has no external verifier. This is the kernel-level form of the Gödel self-reference problem. FRAME (:18085) and the A-auditor role partially mitigate at federation level only, not kernel level — so the risk is real but not absolute.

## How §11 was forged (the procedure, precedent)

1. Append a new §N to `/root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md`. NEVER rewrite existing sections — breaks git blame + seal chain. (Confirmed: file was 491 lines, +96 appended = 587 lines.)
2. `git -C /root/AAA add <file> && git commit -m "feat(doctrine): §11 — 8≠9 invariant, kernel×atlas asymmetry with promotion criterion"` → commit `98a65eed`
3. `python3 /root/HERMES/scripts/zen/git_to_vault.py` → ingest `COMMIT-AAA-98a65eed0bf9`
4. Verify via `tail -1 /root/arifOS/VAULT999/outcomes.jsonl` (round-trip closed)

## Earlier artifacts this session produced (working tree, sealed)

- `AAA/a2a-server/agent-cards/harnesses/opencode.json` + `public/a2a/opencode.json` → `priority: "PRIMARY"`, `replaces: ["codex","claude-code"]`, `bound_to: "333-AGI"`. ⚠️ Field semantics drift risk: `replaces` reads like deletion to downstream consumers; prefer `routing_priority` + `fallback_to` on next pass.
- `AGENTS.md` L752+ and `AAA/instructions/reality-first.md` L53+ → "Harness Routing — Primary & Secondary" section, sovereignty gradient table, 4-dim tensor, ART-ACT-AUTH as gates.
- ⚠️ Working tree committed by sibling but not all changes sealed to VAULT999; only the §11 doctrine patch landed a fresh vault receipt (`COMMIT-AAA-98a65eed0bf9`).

## What this session decided NOT to do

- ❌ Spawn 9×9 = 81 agents (anti-Meta-Mesa).
- ❌ Delete vendor harnesses (sovereignty ≠ autarky).
- ❌ Promote 111 EXPLORER before 5+ independent missions.
- ❌ Add `arif_audit`/`arif_verify`/`arif_explore` verbs (insufficient evidence).
- ❌ Treat ART/ACT/AUTH as atlas buckets (they are temporal gates).
- ❌ Reify "Federation of Species" as constitutional rank (collapses anchor; slot federation instead).

## Cross-references

- Parent skill: `/root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` §11
- Sibling skill (verification pattern): `verify-sibling-ops-reports` — extended this session to cover doc-edit claims, not just cleanup ops
- Atlas doctrine: `arifos-cognitive-atlas` SKILL.md
- Kernel canon: `arifOS/VAULT999/forge/2026-06-19/kernel-bundle/KERNEL_INVARIANT_v1.0.md` — "Runtime problem, not model problem" precedent (line 211)
