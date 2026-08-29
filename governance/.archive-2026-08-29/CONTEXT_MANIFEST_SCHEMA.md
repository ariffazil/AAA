# Context Manifest Schema — WAJIB 8

> **Every durable context artifact must declare its authority class.**
> Agents cannot upgrade guidance to policy by placing it in a privileged path.
> **Forged:** 2026-07-19

## Context Classes

| Class | Meaning | Authority | Expiry |
|-------|---------|-----------|--------|
| **Observation** | Evidence about current state | Agents may append | 24h or explicit |
| **Operational handoff** | Temporary work continuation | Scoped, expiring | Session or 7d |
| **Guidance** | Non-binding recommendation | Agents may propose | 30d default |
| **Policy** | Binding behavioural rule | Kernel-governed review | Explicit only |
| **Constitution** | Changes authority or floors | F13 ratification | Indefinite |
| **Memory** | Historical record | Append-only with provenance | Indefinite |

## Manifest Schema

```json
{
  "context_manifest": {
    "artifact_id": "string — unique identifier",
    "class": "Observation | Operational handoff | Guidance | Policy | Constitution | Memory",
    "author": "string — agent or human identity",
    "source_commit": "string — git commit at creation",
    "authority_level": "advisory | binding | constitutional",
    "approved_by": "string | null — who ratified (required for Policy/Constitution)",
    "binding": false,
    "created_at": "ISO8601",
    "expires_at": "ISO8601 | null",
    "constitution_compatibility": "string — constitution hash this was written under",
    "supersedes": "string | null — artifact_id this replaces",
    "content_hash": "sha256:..."
  }
}
```

## Enforcement Rules

1. **Unapproved agent-authored material loads as advisory, never binding.**
2. **Guidance cannot become Policy without kernel review + approve_by field.**
3. **INIT/NEXT_AGENT_INIT files are Operational handoff (Class 2) — scoped, expiring.**
4. **Constitution changes require F13 ratification (Class 5).**
5. **Memory is always append-only with provenance (Class 6).**

## Boot Path Audit

Existing files that need manifest classification:
- `/root/AAA/prompts/INIT.md` → Operational handoff
- `/root/AAA/prompts/NEXT_AGENT_INIT.md` → Operational handoff
- `/root/AAA/prompts/SALAM_AAA_INIT.md` → Operational handoff
- `/root/AAA/docs/DESIRED_STATE.md` → Guidance (DRAFT TARGET STATE)
- `/root/AAA/docs/REALITY_AUDIT_2026-07-19.md` → Observation/Evidence
- `/root/AAA/governance/*.md` → Policy (kernel-governed)
- `~/.copilot/session-state/*/plan.md` → Operational handoff (session-scoped)
