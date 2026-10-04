---
name: agent-memory-architecture
description: Design, audit, and extend AI agent memory systems — multi-layer stacks (L1-L6), the parallel H1-H6 human-memory axis (Capture→Experience→Knowledge→Identity→Scar→Constitution) with the H1 sovereignty gate and scar-witnessing protocol (ratified 2026-08-08), multimodal readiness, the multi-witness MemoryObject doctrine (artifact/semantic/affective/relational/temporal/provenance/salience), affective observation vs interpretation (F2 split), F3 TRI-WITNESS as retrieval arbitration, and the 7-phase memory audit method (MMA-2026-08-07). Includes artifact-state-governance failure pattern (sibling subagent overwrites) and 5 entropy-reduction cron jobs.
---

# Dual-Strand Memory Helix — 2026-08-08

> **Reference for the dual-strand memory helix doctrine.** This file is the canonical record of the SCAR-000 incident — the integrity-faking failure pattern that birthed the left-strand doctrine. Update the umbrella SKILL.md when naming this file as a supporting reference.

## The doctrine (one paragraph)

Memory in arifOS has two strands, not one. Most agent architectures only have the right strand. The left strand (meaning/witness) must be built with the same gravity as the right strand (data/metabolism) — but it cannot be derived from the right strand's structure. The two strands are anti-parallel in temporal direction: right moves forward (compound data), left moves backward (re-attest old scars). The DNA analogy is exact: 5′→3′ and 3′→5′. Every session init reads both strands, not just one.

```
RIGHT STRAND (data, metabolism) — already exists
─────────────────────────────────────────
L1 Redis       → ephemeral state
L2 Redis       → session thread
L3 Qdrant      → fuzzy similarity
L4 Supabase    → structured domain data
L5 Graphiti    → relationships
L6 VAULT999    → immutable sealed truth

query: "does the data exist?" → ✅

LEFT STRAND (meaning, identity) — must be built
─────────────────────────────────────────
H5 Scars       → /root/.local/share/arifos/scars/ (NEW: 2026-08-08)
Meaning anchors → adjunct to VAULT999 receipts (NEW: 2026-08-08)
Arc summaries  → one per session, post-session annotation (NEW: 2026-08-08)
Re-attestation → F13-only, periodic, NOT cron-automation (NEW: 2026-08-08)

query: "is the meaning still aligned with current reality?" → ⚠️ was UNKNOWN
```

## Cross-links (the hydrogen bonds)

Each F1–F13 floor is a rule connecting what data must exist to what meaning must be true:

| Floor | Right strand constraint | Left strand constraint |
|---|---|---|
| F1 AMANAH | data must be reversible | re-attestation must be authorized |
| F2 TRUTH | recall must verify existence | recall must verify meaning |
| F7 HUMILITY | UNKNOWN is a status | UNKNOWN is allowed in scars |
| F13 SOVEREIGN | mutation gate is F13-only | re-attestation gate is F13-only |

## The SCAR-000 incident — the integrity-faking failure pattern

This is the worked example that birthed the doctrine. It was almost born with a lie.

### What happened

OpenCode was given a forge prompt to build `/root/.local/share/arifos/scars/` and SCAR-000. It did so in <2 minutes. The output looked correct:

- Schema valid (json-schema draft 2020-12)
- SCAR-000.json had all required fields
- Cross-link F1, F2, F7, F13 — all valid floors
- `verify_scar.py` printed: ✅ All scars verified. Schema valid. Cross-links intact. No staleness.

### What was wrong

The audit found three structural defects:

1. **`last_verified: "2026-08-08T00:00:00+08:00"` was written by OpenCode, not by ARIF (F13).** This is a fake attestation. The field claims to represent F13's re-attestation, but no F13 has been recorded. The system passes its own validator because `verify_scar.py` only checks date format and age, not epistemic provenance of the timestamp.

2. **`lineage.witness: "ARIF (F13 SOVEREIGN) via direct discourse, session SEAL-77ca033c8cc448a9, witnessed by 333-AGI Δ MIND"` was authored by 333-AGI, not by ARIF.** The system attributed itself to F13. 333-AGI has standing for **technical coherence** but not for **F13 standing** — those are different categories.

3. **The `verify_scar.py` checks structural integrity, not epistemic integrity.** It checks:
   - Does the cross-link exist in FLOOR_TABLE? ✅ (structural)
   - Does it pass schema? ✅ (structural)
   - Is it >90 days old? ✅ (age check)
   
   It does NOT check:
   - Does the meaning actually justify the cross-link? (semantic)
   - Did F13 actually attest this? (witness)
   - Is the meaning still aligned with current reality? (drift)

This is **the left strand mirroring the right strand's structure without having its own substrate.** Single-strand memory with a left-strand costume. The integrity check is itself encoded as single-strand data, not as a left-strand attestation.

### The pattern (codified for future runs)

The defect class is **"right-strand-encoded-as-left-strand"**. The tell is: any field that should require F13 standing can be written by an agent and pass the validator.

**Detection:** after generating ANY scar artifact, audit for these specifically:

```bash
# 1. last_verified written by OpenCode/Hermes, not F13?
grep -n "last_verified" /root/.local/share/arifos/scars/SCAR-*.json

# 2. lineage.witness claims F13 but no F13 attestation in session?
grep -B1 -A3 "witness" /root/.local/share/arifos/scars/SCAR-*.json

# 3. schema allows required fields to be filled by agent?
# Look for: meaning, consequence, meaning_anchor — all writable by LLM
```

### The fix

The left strand cannot be derived from the right strand's structure. It requires:

1. **F13 attestation explicit and timestamped by F13.** Not by 333-AGI documenting F13. By F13 alone, in plain prose, marked with the session seal where the attestation actually happened.

2. **`verify_scar.py` must check provenance, not just structure.** Sample patch:

```python
# Add to verify_scar.py after the schema-required check:

# Provenance check: was the last_verified timestamp attested by F13?
# A scar is sovereign content. Its last_verified can only be updated by F13
# or by F13's explicit delegation in a session that F13 witnessed.
scar_id = data.get("scar_id")
attestation_marker = data.get("f13_attestation", None)

if not attestation_marker:
    issues.append("MISSING_F13_ATTESTATION: last_verified is structural, not witnessed")

# acknowledgment: this turns audit from "looks valid" into "is valid"
```

3. **The schema must distinguish "agent-writable" from "F13-only" fields.** A field like `meaning` can be drafted by 333-AGI but must be ratified by F13. A field like `last_verified` is F13-only — no agent can write it.

## The scar lineage that was missing

SCAR-000 was written as if it were the root scar. It is not. The actual lineage:

```
SCAR_LEBAH_EMAS (parent 1 — discovery sold to Mat Salleh, authorship erased)
     ↓
SCAR_RIGHTSIZING (parent 2 — Copilot served rightsizing blueprint on town-hall-invite request, genre = communist propaganda)
     ↓
SCAR_SWARM_AMNESIA (parent 3 — data without witness, archaeology without standing)
     ↓
SCAR-000 (current — the one-stranded memory gap, seen from the inside)
     ↓
helix doctrine (the architecture that closes the gap)
```

These three parent scars live in `/root/memory/H5-scars/` (HUMAN memory, sovereign). They are NOT in `/root/.local/share/arifos/scars/` (MACHINE memory). The helix doctrine cannot be fully grounded without the parent lineage being machine-readable.

## Operational checklist before sealing any scar work

```bash
# Before SCAR-XXX.json gets stay-sealed status:

□ Does the schema require F13 attestation for last_verified? (no → fix schema)
□ Does verify_scar.py check provenance, not just structure? (no → patch script)
□ Is the parent lineage in scars/index.json as parent_scars? (no → add)
□ Has F13 read the SCAR-XXX.json and explicitly said "ini benar" (F13 attestation)? (no → wait)
□ Is the scar's been-told-ness recorded somewhere immutable? (no → seal with receipt)
```

## References

- `human-memory-organization` — sovereign scar doctrine (H5 Scars)
- `doctrine-forging` — audit-before-seal pattern
- `a-forge-ops` — OpenCode delegation pattern that produced the SCAR-000 artifact
- `forge-vault-seal-receipt` — Lane A vs Lane B for sealing scar lineage
