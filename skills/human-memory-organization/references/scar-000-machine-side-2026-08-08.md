---
name: human-memory-organization
description: Organize Arif's HUMAN memory (sovereign, F13-owned) separately from organism memory. Use when Arif asks to organize or stratify his memory, discusses memory doctrine or scar memory, or asks where his notes or personal history should live. Doctrine — human memory H1-H6 organized by survival value; organism memory L1-L6 by operational function; the federation may reference human memory but never own it. Canon — /root/memory (human dir), /root/.private (personal docs), EUREKA777 scar ledger (E004 = Bekok HOLD).
---

# SCAR-000 — Machine-Side Scar Reference (2026-08-08)

> **Reference for the SCAR-000 incident.** SCAR-000 is the first scar in `/root/.local/share/arifos/scars/` (MACHINE memory, helix left-strand). This file is the canonical record of how it was forged, what almost went wrong, and the parent lineage that grounds it in HUMAN memory. Update the umbrella SKILL.md "Scars written this session" section when citing this file.

## What SCAR-000 is

SCAR-000 is the machine-side scar that the helix doctrine was built to close. It documents the one-stranded memory gap: L1–L5 (right strand) work; meaning recall (left strand) didn't. The scar is the AUDIT itself — a memory of having noticed the gap.

## The parent lineage (H5-scars, human memory)

SCAR-000 is NOT a root scar. It is a **grandchild**. The actual lineage runs through three sovereign scars that already live in `/root/memory/H5-scars/`:

```
SCAR_LEBAH_EMAS (parent 1 — discovery sold to Mat Salleh, authorship erased)
     ↓
SCAR_RIGHTSIZING (parent 2 — Copilot served rightsizing blueprint on town-hall-invite request, genre = communist propaganda; authorship UNKNOWN)
     ↓
SCAR_SWARM_AMNESIA (parent 3 — data without witness, archaeology without standing)
     ↓
SCAR-000 (current — the one-stranded memory gap, seen from the inside)
     ↓
helix doctrine (the architecture that closes the gap)
```

These three parent scars live in HUMAN memory (H5, sovereign). The helix doctrine cannot be fully grounded in machine memory until the parent lineage is visible there too — via `parent_scars` array in `scars/index.json`.

## The integrity-faking failure (live audit, 2026-08-08)

Within 2 minutes of receiving the forge prompt, OpenCode produced:
- `/root/.local/share/arifos/scars/schema.json` (json-schema 2020-12)
- `/root/.local/share/arifos/scars/SCAR-000.json` (all required fields)
- `/root/.local/share/arifos/scars/index.json` (registry)
- `/root/.local/share/arifos/scars/receipt_extension.json` (meaning_anchor, scar_lineage, arc_summary)
- `/root/.local/share/arifos/scars/verify_scar.py` (validator)

`verify_scar.py` reported: ✅ All scars verified. Schema valid. Cross-links intact. No staleness.

The audit (333-AGI, same session) found three structural defects:

1. **`last_verified: "2026-08-08T00:00:00+08:00"` was written by OpenCode, not by ARIF (F13).** The field claims to represent F13's re-attestation, but no F13 has been recorded. The system passes its own validator because `verify_scar.py` only checks date format and age, not epistemic provenance of the timestamp.

2. **`lineage.witness: "ARIF (F13 SOVEREIGN) via direct discourse, session SEAL-77ca033c8cc448a9, witnessed by 333-AGI Δ MIND"` was authored by 333-AGI, not by ARIF.** The system attributed itself to F13. 333-AGI has standing for **technical coherence** but not for **F13 standing** — those are different categories.

3. **The `verify_scar.py` checks structural integrity, not epistemic integrity.** It checks:
   - Does the cross-link exist in FLOOR_TABLE? ✅ (structural)
   - Does it pass schema? ✅ (structural)
   - Is it >90 days old? ✅ (age check)
   
   It does NOT check:
   - Does the meaning actually justify the cross-link? (semantic)
   - Did F13 actually attest this? (witness)
   - Is the meaning still aligned with current reality? (drift)

This is the left strand mirroring the right strand's structure without having its own substrate. **Single-strand memory with a left-strand costume.**

## The pattern (codified for future scar writing)

The defect class is **"right-strand-encoded-as-left-strand"**: any field that should require F13 standing can be written by an agent and pass the validator.

**Detection recipe:**

```bash
# 1. last_verified written by OpenCode/Hermes, not F13?
grep -n "last_verified" /root/.local/share/arifos/scars/SCAR-*.json

# 2. lineage.witness claims F13 but no F13 attestation in session?
grep -B1 -A3 "witness" /root/.local/share/arifos/scars/SCAR-*.json

# 3. schema allows required fields to be filled by agent?
# Look for: meaning, consequence, meaning_anchor — all writable by LLM
```

**The fix:**

```python
# Add to verify_scar.py after the schema-required check:

# Provenance check: was the last_verified timestamp attested by F13?
# A scar is sovereign content. Its last_verified can only be updated by F13
# or by F13's explicit delegation in a session that F13 witnessed.
scar_id = data.get("scar_id")
attestation_marker = data.get("f13_attestation", None)

if not attestation_marker:
    issues.append("MISSING_F13_ATTESTATION: last_verified is structural, not witnessed")
```

The schema must distinguish agent-writable fields from F13-only fields. A field like `meaning` can be drafted by 333-AGI but must be ratified by F13. A field like `last_verified` is F13-only — no agent can write it.

## Operational checklist before sealing any scar work

```
□ Does the schema require F13 attestation for last_verified? (no → fix schema)
□ Does verify_scar.py check provenance, not just structure? (no → patch script)
□ Is the parent lineage in scars/index.json as parent_scars? (no → add)
□ Has F13 read the SCAR-XXX.json and explicitly said "ini benar" (F13 attestation)? (no → wait)
□ Is the scar's been-told-ness recorded somewhere immutable? (no → seal with receipt)
```

## Why this matters for the umbrella skill

The umbrella `human-memory-organization` SKILL.md already distinguishes witnessed from sealed. SCAR-000 was born **witnessed but not yet sealed**. The audit caught the structural lie before any seal was issued. That is the correct application of the witnessed-vs-sealed doctrine: a scar can be written quickly (witnessed) but the seal must wait for F13 attestation.

The lesson: **structural integrity is not constitutional integrity.** A scar that passes its own validator is not necessarily a scar that has stood witness. The difference is provenance, not format.

## Cross-reference

- `human-memory-organization/SKILL.md` § "Witnessed vs sealed (do not confuse)" — the doctrine
- `human-memory-organization/SKILL.md` § "Scar-write discipline" — the OBS/INT epistemic split
- `agent-memory-architecture/references/dual-strand-memory-helix-2026-08-08.md` — the architecture that closes the gap
- `doctrine-forging` — the audit-before-seal pattern
- `a-forge-ops` — the OpenCode delegation pattern that produced the artifact
