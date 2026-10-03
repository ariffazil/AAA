# LESSON-2026-10-03 — arifOS checkout-branch deploy + stale SOT copies evidence

> **Status:** DRAFT_LESSON (institutional note — evidence + falsifiable rule, not doctrine)
> **Filed:** 2026-10-03 · **By:** FI-008 (kimi-code), sesi `SEAL-ddf5fe51f3cf465b` / `SEAL-9c657ad6a0184085`
> **Why this file exists:** kernel memory `arif_memory` write is lease-gated (L13) — this AAA file is the durable record instead.

## Lesson 1 — deploy-release.sh ships the CHECKED-OUT branch
`/root/arifOS` working checkout is on `feat/truth-metabolism-no-data-is-not-all-clear`, NOT main. `scripts/deploy-release.sh` builds from the working tree, so a "reconcile source==built==deployed" deploy ships whatever branch is checked out (2026-10-03: feature tip `c766210` = origin/main `f3b451d3` + 9 feature commits; deploy PASS strict, all gates green).

**Rule:** before any arifOS deploy or "push main" claim, run `git -C /root/arifOS branch --show-current` first. Local main == origin/main == `f3b451d3` (verified). Feature→main merge belongs to the feature lane (FI-003/333-AGI), not the reconciling lane.

**Also:** arifOS has a fail-closed pre-push "KERNEL DEPLOY GUARD" hook (pytest E2E + defect detectors + drift gate, ~26s) — push latency there is the gate working, not a hang.

**Falsifier:** if a future deploy shows the checked-out branch is main and drift still occurs, this lesson's cause model is wrong.

## Lesson 2 — "federation-models.json" SOT has stale twins (evidence, recorded not deleted)
Runtime consumer (verified): `fed_router.py:271` → `FED_SOT_PATH = /root/.config/federation-models.json` (`656f0ebf…`, 323,371B — matches cross-audit pin).

Unreferenced stale copies (hash differs, no code reads them — grep across arifOS docs/, sa-fix/, A-FORGE src found zero consumers):
- `/root/arifOS/docs/federation-models.json` — `68ad7f09…`, 198,099B
- `/root/forge_work/sa-fix/docs/federation-models.json` — `68ad7f09…`, 198,099B

**Action taken:** recorded here only. Deletion/cleanup belongs to the owning lanes (arifOS docs tree sits on FI-003's feature-branch checkout; sa-fix is a fix workspace). Same failure-class as the unguarded litellm YAML (see A-FORGE `scripts/hooks/pre-commit/litellm_dangling_guard.py`, built same day).

**Falsifier:** if any runtime is later shown to read the docs/sa-fix copies, this record is wrong and the copies are NOT stale.
