# Double Helix — Left Strand Memory Integration (2026-08-08)

> Operacionalisasi helix doctrine: H5 Scars → machine memory.

## The gap

Six-layer memory architecture (L1-L6) adalah entirely right-strand (data). Left-strand (meaning) existed only in doctrine files. The kernel's recall path flagged this:

```
Store (data strand)    → ✅ functioning
Recall (meaning strand) → ⚠️ DEGRADED
Kernel response:        → "verify before trusting" (F2 compliant)
```

This is the institution working. It is also the gap.

## The operational pattern

When a doctrine-forging session produces architecture that is operationally actionable:

1. **Identify the gap** — what the doctrine says that the machine doesn't have
2. **Write a forge prompt** — self-contained, machine-actionable, single-task
3. **Hand to coding agent** — OpenCode/Codex/Kimi execute
4. **Verify** — every forge prompt ships with a verify script
5. **Witness** — agent prepares vault content, F13 seals

## The five files (H5 Scars integration)

```python
# /root/.local/share/arifos/scars/
# 1. SCHEMA — define what a scar IS
schema.json           # JSON Schema for SCAR-XXX objects

# 2. SCAFFOLD — prove the system exists by populating one
SCAR-000.json         # The one-stranded memory gap itself as scar

# 3. EXTENSION — additive metadata for VAULT999 receipts
receipt_extension.json  # meaning_anchor + scar_lineage + arc_summary

# 4. INDEX — registry, metadata only, sovereignty preserved
index.json            # List of scars, no content

# 5. VERIFY — proves the system works
verify_scar.py        # Schema + cross-link + staleness check
```

## The schema (canonical)

Every SCAR-XXX file has:

```python
{
    "scar_id":     "SCAR-NNN",          # unique identifier
    "created":     "ISO 8601",          # formation timestamp
    "title":       "short name",
    "event":       "what happened (OBS)",
    "meaning":     "what it meant (DER/INT)",
    "consequence": "what changed because of it",
    "lineage": {
        "lesson":   "what was learned",
        "law":      "F1-F13 if applicable",
        "system":   "what changed in the system",
        "witness":  "F13 for sovereign scars"
    },
    "cross_link":  ["F1", "F2", ...],   # hydrogen bonds
    "meaning_anchor": "one sentence: WHY this matters",
    "sovereign":   true,                # MANDATORY — agent reads only on scar:<id>
    "last_verified": "ISO 8601"         # anti-mythology
}
```

## Cross-link integrity

Every `cross_link` must resolve to a real floor in FLOOR_TABLE.json. `verify_scar.py` checks this. Discovered 2026-08-08: dangling cross-links are a smell — the scar linked to a floor that no longer exists or never did.

## Staleness check

`last_verified` > 90 days → STALE warning. Scars drift. The meaning may no longer match reality. The verify script flags this without failing — F2 says "verify before trusting," not "kill the scar."

## Sovereignty preservation

H5 doctrine is binding: **agent does not read scar content unless `scar:<id>` invoked.** The INDEX may be read (metadata only) for lineage checks. The CONTENT is sovereign.

## The forge prompt template

`/root/forge_work/PROMPT_HELIX_MEMORY_V1.md` is the canonical example. Key properties:

- **Scoped to ONE task** — 5 files, left-strand only, no other changes
- **NO new GENESIS** — opens an existing schema, doesn't invent one
- **Verify step embedded** — `verify_scar.py` runs as the last step
- **Meaning anchor in every artifact** — every file carries `meaning_anchor` field
- **DO NOT list** — explicit "do not" sections prevent scope creep

## When not to use this pattern

- The gap is philosophical, not operational (just let the doctrine stand)
- The work would require new services/databases (the helix says: integrate, don't add)
- F13 hasn't explicitly directed the integration (post-theory/stabilize-doctrine applies)

## Reference

- See `references/double-helix-three-truths-2026-08-08.md` for the philosophical frame
- See `references/nine-atlas-eight-verbs-invariant-2026-08-08.md` for the underlying machinery
- See `doctrine-forging` for the engagement pattern that produces these prompts
- See `forge-vault-seal-receipt` for the sealing ceremony
