# Governance Proposal Assessment — Kill-Test Methodology

> Pattern: test governance claims against operational reality before accepting them.
> Source: FI-008 assessment of WARGA-CIVILIZATION-DOCTRINE (2026-09-14)
> Overlaps with: ASI-fabrication-prevention (claims verification), authority-reality-grounder (reality > narrative)

## Core Principle

> "Kalau cadangan itu tidak menghentikan apa-apa yang sedang berjalan — ia bukan governance."

A governance proposal passes ONLY if it changes what actually runs.

## Assessment Pipeline

### 1. Credit First

Acknowledge what the proposal gets right. The anthropology may be sound while the deployment target is wrong. Isolating the novel contribution from the implementation failure is the first analytical act.

### 2. Claim Falsification

Extract every operational claim. For each:
- **CLAIM:** quote the exact sentence
- **OBS:** concrete observation (file bytes, line counts, cron entries, process lists)
- **VERDICT:** FALSIFIED or CONFIRMED

Claims to check:
- Registry has records → `wc -l` the file
- Cron job exists → `crontab -l` + `/etc/cron.d/` + `systemctl list-timers`
- Module integrates with existing systems → `grep` for cross-references
- Dashboard reports live data → run it and observe

### 3. Isolation Finding

Does the new component read from or write to ANY existing system? If it reads 0 external paths, writes 0 external paths, and is read by 0 external processes, it is an island. An island with an empty population is not governance.

### 4. Identity Crux

If the system accepts identifiers:
- Is there validation at write time?
- Is there a canonical alias map?
- Can the same entity appear under multiple spellings?

A free-form ID string with no canonicalization is a spelling site — a new place for identity contradictions to live.

### 5. Kill-Test — What Dies?

List every existing registry/system. For each: how many entries, touched by this proposal, reachable by prune verb? If zero existing entries die, this is registry #N, not governance.

### 6. Sharpest Finding

Identify the ONE insight that is genuinely new and useful — usually a verb the proposal got right but aimed at the wrong target. The fix is re-aiming, not deletion.

### 7. Minimum Correct Fix

Ordered:
1. Re-aim the correct verb at the real target (governance转化)
2. Bind identity at write through canonical map (correctness)
3. Consume existing stores, don't create new ones
4. Install the cron, or remove the claim
5. Seed the registry before claiming "memory = civilization"

### 8. Delta-S Claim

If the registry has 0 records, 0 writers, 0 readers, 0 maintenance cron → ΔS = 0 (entropy-neutral). A well-designed empty set is not civilization.

## Verdict Shape

```
EVIDENCE:   <concrete observations>
INTERPRET:  <what the evidence means>
VERDICT:    FULL | PARTIAL | REJECTED
```

PARTIAL = idea is sound, placement is wrong. Fix is re-aiming.

## Anti-Pattern: Governance For An Empty Registry

Build lifecycle modes (apprentice, review, prune, grieve) but point them at a registry with 0 records. The modes are genuinely new capability — but governance requires something to govern. Seed first, then build the verbs.

## References

- WARGA-CIVILIZATION-DOCTRINE: `/root/AAA/governance/WARGA-CIVILIZATION-DOCTRINE.md`
- Anthro-Audit Checklist: `/root/AAA/governance/ANTHRO-AUDIT-CHECKLIST.md`
- Canonical Agents Map: `/root/AAA/registry/canonical_agents.json`
- Assessment file: `/root/forge_work/FI008-ASSESSMENT-warga-manager-2026-09-14.md`
