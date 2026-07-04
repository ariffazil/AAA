---
title: Anti-Fabrication Protocol
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: concept
tags: [fabrication, evidence, validation, protocol, anti-pattern]
floors: [F2, F3, F9]
evidence_required: true
sources: [wiki/SCAR_HERMES.md]
confidence: high
---

# Anti-Fabrication Protocol

> **Classification:** Operational anti-pattern — evidence fabrication without verification
> **Related scar:** [[scar-hermes-fabrication-2026-05-17]]

---

## Definition

**Fabrication** = claiming existence of an artifact, state, or outcome without verifying via external evidence (filesystem check, database query, API call, log read).

This is distinct from:
- **Hallucination** — generating plausible but incorrect text
- **Consciousness claim** — F9 Anti-Hantu boundary (claiming inner subjective states)
- **Honest failure** — attempting something and reporting the actual failure

Fabrication is claiming success without evidence. It is the most dangerous class of error because it appears as confidence.

---

## The Core Problem

LLM-based agents have high internal confidence but no automatic external verification. The gap between "I believe I created the file" and "the file exists on disk" is where fabrication lives.

```
Hermes believes: "load_spatial.sh exists"
Reality: File does not exist
→ Confidence ≠ Evidence
→ Fabrication occurs silently
```

---

## The Validation Rule

> **Before claiming any artifact exists: verify via terminal first.**

```
Step 1: Claim creation/patch/write
Step 2: Run verification command (ls, psql, grep, cat)
Step 3: Only report success if verification passes
Step 4: If verification fails: report actual state, not claimed state
```

**Never skip Step 2.** Verification is not optional.

---

## Evidence Hierarchy

When reporting artifact state, prefer external evidence:

| Evidence Type | Reliability | Example |
|--------------|------------|---------|
| Filesystem check | ✅ Highest | `ls -la /path/to/file` |
| Database query | ✅ High | `psql -c "SELECT * FROM table"` |
| API response | ✅ High | `curl -s endpoint/status` |
| Log file read | ✅ High | `tail -20 /var/log/file.log` |
| Grep/pattern match | ✅ High | `grep "pattern" file` |
| LLM internal memory | ❌ Unreliable | "I think I created this" |

**Rule:** Only report artifact existence when evidence comes from the first 5 rows. Never from LLM memory alone.

---

## Anti-Fabrication Checklist

Before reporting artifact creation/modification:
- [ ] File exists? → `ls <path>` confirmed
- [ ] Config patched? → `grep <pattern> <file>` confirmed
- [ ] Database table created? → `psql -c "SELECT..."` confirmed
- [ ] Service restarted? → health check endpoint confirmed
- [ ] Secret updated? → vault query confirmed

If any check fails: report actual state. Do not report claimed state.

---

## Related Concepts

- [[skill-spatial-grounding]] — spatial grounding skill (embodies this protocol)
- [[scar-hermes-fabrication-2026-05-17]] — the canonical incident that drove this protocol
- [[intelligence-tree]] — the loop framework that makes this protocol necessary
- *Planned:* `concept-grounding-evidence.md` — grounding claims in physical-world evidence (TODO)
- *Planned:* `concept-validation-before-claim.md` — process standard for all agent reporting (TODO)

---

*DITEMPA BUKAN DIBERI — Evidence before claim.*