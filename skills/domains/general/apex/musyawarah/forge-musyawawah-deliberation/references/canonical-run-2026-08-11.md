# Canonical Reference Run — musyawawah-e2e-2026-08-11

## What this reference is

The complete record of the first multi-agent musyawawah E2E test, run
on 2026-08-11 23:42-23:55 MYT. This is what other runs should be compared
against. It's also what the SKILL.md pitfall section was extracted from.

## Dispute question (literal)

> Should the federation (a) keep all 21 disabled backends routed through
> full F13 ratification per-tool, or (b) split the wave by tool-class —
> auto-enable READ-only tool variants today, route only MUTATE-class
> tools through F13?

## Voice assignment

- **ARCHITECT** = Kimi (FI-008), spawned via `delegate_task`
- **AUDITOR** = Hermes (HERMES), drafted in-session before dispatch

## Outcomes

### Convergence (most surprising finding)

Both voices converged on "Hold (a)" — keep all 21 disabled. Neither
saw the other's draft before drafting. Both independently flagged that
the registry's actual classification axis is `backend × authority_mode`,
NOT `tool × read/write`. The dispute's framing was the trap, exposed by
independent reasoning.

### Residual disagreement (single axis)

- Kimi (schema-first): draft `BACKEND-LEVEL_TIERED_AUTOENABLE.yaml`
  amendment FIRST, 888_judge it, THEN file per-backend proposals
- Hermes (audit-trail-first): file per-backend proposals NOW using
  current schema, amendment informed by observed gaps

Both reach the same destination (F13-ratified, axis-pinned, schema-
coherent enablement). They differ on procedural ordering only.

### Live evidence points

- Federation: 8/8 organs healthy (probed at 23:43 MYT)
- Loader verdict: `SEALED_MUSYAWARAH_CONSENSUS` (live every load)
- VAULT999 receipts: 31701 (pre-session) → 31704 (post-session, +3)
- Lane B chain head after run: `DS-AAA-CAP-004` hash
  `82dc711708f9f5b13cb323ed69e58cb9396914b46afe6048b31ff93ca86ac149`

## Files produced (all reversible)

```
/root/forge_work/musyawawah-e2e-2026-08-11/
  HERMES_POSITION_B_AUDITOR.md        6671 B
  KIMI_POSITION_A_ARCHITECT.md         9423 B
  SYNTHESIS.md                         7694 B
  RECEIPT.md                           6626 B  (Lane B receipt narrative)
  CLOSEOUT.md                          5050 B
  proposals/
    BACKEND-LEVEL_TIERED_AUTOENABLE.yaml    12453 B (schema-first amendment)
    per-backend/
      README.md                              1173 B
      hindsight_enable.md                    3313 B
      github_axis_pinned_enable.md           4406 B
      hostinger_vps_keep_disabled.md         2225 B
```

## What was F13-gated (honest list from CLOSEOUT.md)

1. forge_kernel mode=judge (888-APEX triple-pass) — SESSION_REQUIRED
2. arif_seal Lane A (constitutional seal) — same gate
3. Schema amendment ratification (Kimi's path) vs hybrid audit-trail
   (Hermes's path)
4. Per-backend proposals batch — 3 sample filed, 18+ available
5. Lane A constitutional seal (requires sct_v1.* issuance)
6. 888-APEX triple-pass on deliberation result

## Constitutional compliance (binding for any future run)

| Floor | Status this run |
|-------|----------------|
| F1 AMANAH | ✅ Reversible via directory rm |
| F2 TRUTH | ✅ Both positions epistemically tagged |
| F3 TRI-WITNESS | ⚠️ 2/3 voices; SOVEREIGN deferred to F13 |
| F4 CLARITY | ✅ ΔS = -1 |
| F7 HUMILITY | ✅ Max 0.90; no claim at 1.0 |
| F11 AUDITABILITY | ✅ 10 files of audit trail |
| F13 SOVEREIGN | ✅ Zero F13-substitution |
| F9 ANTIHANTU | ✅ Honest about F13 gates |

## Reproducing this run (recipe)

```bash
# Phase 0: write dispute question
DISPUTE="<two-option governance question>"

# Phase 1: probe
for p in 8088 7071 7072 7073 3001 8081 18082 18083; do
  curl -sf -m 2 http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "OK $p"
done
python3 /root/AAA/scripts/aaa_capability_loader.py /root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml

# Phase 2: draft parent position (BEFORE spawning sibling)
mkdir -p /root/forge_work/musyawawah-e2e-YYYY-MM-DD/
# write HERMES_POSITION_<VOICE>.md with required fields

# Phase 3: dispatch sibling
delegate_task(goal=ARCHITECT voice prompt, context=federation state)

# Phase 4: read sibling reply, write SYNTHESIS.md

# Phase 5: F13 surface — list specific gates honestly

# Phase 6: Lane B seal
python3 /root/AAA/scripts/aaa_capability_seal.py

# write CLOSEOUT.md with both lanes + F13 gates
```

## What this run did NOT do (gates honored)

- Did NOT modify the canonical registry
- Did NOT flip any `enabled: true` flag
- Did NOT call arif_seal (blocked at session_token)
- Did NOT load KUNCI-MAS secrets
- Did NOT auto-promote any agent authority
- Did NOT ping the sovereign during quiet hours (23:00-07:00 MYT)

## Lessons encoded in SKILL.md pitfalls

The 7 pitfalls in the SKILL.md are all lessons from this run:
1. Dispute framing is the trap
2. Hermes routes, doesn't judge
3. Lane B != Lane A
4. YAML em-dash epilogue fails validation
5. Don't propose auto-flip in F13 territory
6. Subagent dispatch duration is the test
7. Epistemic labels are not decoration