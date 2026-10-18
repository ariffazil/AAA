# SCAR-2026-10-18-003 — Stale Audit Batch: 3/3 P0 Already Fixed

**Filed:** 2026-10-18 by 333-AGI Δ MIND
**Weight:** w_scar = 0.8
**Class:** DOCUMENTATION_DRIFT + WITNESS_THEATRE (audit-side)

## What happened

An `agy-cli/audit` alignment audit (Phase 0–8, read-only, verdict HOLD) proposed
"Mutation Batch 1" with 3 P0 blockers. All 3 were already fixed on disk before
the batch could be authorized:

| Audit P0 | Claim | Live reality 2026-10-18 |
|---|---|---|
| SINK-04 | `ARIFOS_TRUST_AUTO_SIGN_UNKNOWN=1` live in `/etc/systemd/system/arifos.service:30` | **REMOVED today 11:14:49** — proof: `/etc/systemd/system/arifos.service.bak-autosign-20261018-111449` still carries the line; live unit file does not |
| SINK-06 | `tests/conftest.py:400-428` writes mock over `/root/WELL/state.json` | **ALREADY FIXED** — current code uses `tmp_path_factory.mktemp("well_state")` exclusively; `vps_path` symbol absent from file |
| SINK-10 | `litellm-config.yaml:2089-2100` routes `i-arif → [apex-888, forge-777, agi-333]` | **ALREADY FIXED** — live config shows `i-arif: [deepseek-flash, mimo-v2.6-flash, MiniMax-M3.1-Flash-Preview, MiniMax-M3]`; no cross-tier judge/actuator fallback |

P1 status: SINK-03 (arifVerifySealLive) **already fixed** — now calls
`arif_init(mode="validate")` fail-closed. SINK-02 **partially fixed** — nullish
fallback is now `?? (resp.status === "PASS" || resp.verdict === "SEAL")`, not
`?? true`. SINK-05 **STILL REAL** (see below).

## Why it matters

An audit that reports present-tense defects without re-probing at authorization
time produces a batch that, if applied, would:
- re-introduce nothing (no-ops at best),
- burn sovereign attention on already-closed items (HumanLeverage ↓),
- and create false confidence that "P0 is handled" while the genuinely live
  defect (SINK-05) sits unfixed.

This is the audit-side instance of the federation's own law:
**present tense is a claim, not a status.**

## The one real defect confirmed live

`/root/A-FORGE/src/interfaces/mcp/shell/forgeShell.ts:137`

```ts
function matchScarsByKeywords(command: string): ScarHit[] {
  try {
    if (!existsSync(SCAR_RUNTIME_INDEX)) return [];   // ← FAIL-OPEN
```

Missing scar index → empty scar list → mutation proceeds unconstrained.
Kernel-side `forge_scar_consult.py` fails CLOSED on the same condition.
The two scar gates disagree on failure semantics.

Falsifier: point `SCAR_RUNTIME_INDEX` at a nonexistent path, issue a mutation
command, observe whether it is blocked (correct) or allowed (defect).

## Binding rule (this scar)

Before presenting any remediation batch for authorization:

1. Re-probe every claimed defect at authorization time, not at analysis time.
2. Report per-item: `STILL_LIVE` / `ALREADY_FIXED (evidence)` / `PARTIAL`.
3. A batch whose items are majority-stale must be re-scoped, not submitted.
4. Audit age > 1 session ⇒ treat all findings as UNVERIFIED until re-probed.

## Related

- scar-2026-10-18-001 (silent-mutation shadow command)
- scar-2026-10-18-002 (LOC reduction without import-graph verification)
- `/root/AAA/instructions/representation-reality-invariant.md`
- `/root/AAA/instructions/frontier-model-audit-verification.md` (probe-to-witness Rule #8)
