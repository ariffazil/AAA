---
name: scar-integration
id: scar-integration
version: 2.0.0-wave2-merged
description: "Capture session failure patterns as constitutional scars — reusable diagnostics that prevent repeat mistakes."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F7, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - wisdom-scar-session-audit (sha256: f168d9ddf0418241b1afabc9393573ba9ea4de65e2e438be4efb81766763586d)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/scar-integration/TOMBSTONE-wisdom-scar-session-audit.json
triggers:
  - "capture wisdom scar"
  - "session failure audit"
  - "scar ledger"
  - "constitutional scar"
attention:
  load_class: medium
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "scar"
    - "failure pattern"
    - "wisdom"
  output_contract:
    - "scar_receipt"
    - "scar_severity"
    - "scar_remediation"
tags: [governance, scar, wisdom, session, F2, F7, F11]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
owned_by: AAA
authority_of: AAA
---

# core/governance/scar-integration

Session failure pattern → constitutional scar promotion. Merged from wisdom-scar-session-audit per Wave 2 APEX verdict.

A scar is a reusable diagnostic that prevents repeat mistakes. Severity: P0-P4 per AGY/SCAR doctrine.

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/wisdom-scar-session-audit/
rm -rf skills/core/governance/scar-integration/
```

## Provenance
- **Wave:** 2, item 10
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Binding a Scar — Provenance Integrity (the scar-catalog discipline)

When converting an observed session defect into a catalog scar, three rules prevent the catalog itself from rotting (Scar #15 — Scar Shadow Paradox).

1. **LANDED ≠ SEAL.** A scar entry recorded in the catalog is LANDED — the diagnostic is captured. A scar becomes SEALED only after next-session behavior evidence shows the discipline fires (i.e. the scar was actually consulted and constrained selection, or it was provably absorbed and never re-fired). Never SEAL a scar at write-time. SEAL is post-hoc evidence, not intent.

2. **Provenance integrity — silent metadata drift is the bug class.** Every scar entry must declare: original date tokens (the actual scar-event date, never re-tagged), the F13-derived session or scar name (e.g. `scar:PRIVACY-DRIFT-2026-10-08` matches the SOUL.md patch token), the source session/event ID, and the affected surface. If a date or token is rewritten during editing, declare the rewrite inline (`[provenance: <new-tag> derived from <old-tag>, reason: …]`). Bare re-tagging without declaration corrupts F2 provenance; future audit queries for the original token return empty and the scar is no longer findable by its real cause.

3. **Patch-stacking is a known scar.** Don't accumulate patches across turns without an interleaved behavior test. Each layer that lands without a fresh-session replay test compounds uncertainty: layer N's behavior depends on layer N-1's behavior, which was never tested. The discipline: **patch → next-session replay → patch → next-session replay**. If a session demands stacked patches (e.g. audience gate + first-ask + privacy non-lecture + scar-cluster compress + energy ledger + sexual-lane + hold-abolition in one session), declare the stack in the LANDED receipt and require a single next-session replay that exercises the entire stack against a 4-trigger battery before any single layer is treated as SEALED.

## Absorbed references (Wave-2 merge completion)
- `references/absorbed-wisdom-scar-session-audit.md` — content absorbed from the retired `wisdom-scar-session-audit` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17). Living scar catalog: #1–#21. Latest additions are Scar #20 (Privacy ≠ Amnesia — Redacted ≠ Unauditable, 2026-10-02) and Scar #21 (Runtime State Machine Correct, Ledger State Machine Stale, 2026-10-02). Scar #20 enforces the two-surface rule (payload retention policy separate from causal-provenance envelope); Scar #21 enforces the runtime-vs-ledger dual audit (a detector's bookkeeping table can lie even when its runtime is correct). Always read this file when the user says "capture wisdom scar", "what did we learn", "session failure audit", "redact / scrub / tombstone", or when a redacted-but-auditable surface is being designed.
