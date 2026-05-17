---
title: "SKILL: Evidence Verification — Generic Protocol"
created: 2026-05-17
updated: 2026-05-17
version: 0.1.0
type: skill
tags: [evidence, verification, validation, fabrication, protocol, generic]
category: governance
risk_band: HIGH
floors: [F2, F3, F9]
evidence_required: true
sources: [wiki/concepts/anti-fabrication-protocol.md, wiki/scar-hermes-fabrication-2026-05-17.md]
confidence: medium
status: stub
---

# SKILL: Evidence Verification — Generic Protocol

> **Skill ID:** `skill-evidence-verification`
> **Canonical location:** `AAA/wiki/skills/skill-evidence-verification.md`
> **Status:** STUB — derived from anti-fabrication-protocol, needs generalization
> **When to use:** Before claiming any artifact exists, any state change succeeded, or any evidence was produced
> **Severity:** HIGH — skipping verification is the root cause of the Hermes fabrication scar

---

## Summary

Generic evidence verification protocol — before claiming any artifact exists or any action succeeded, verify via external check (not LLM memory). This skill embodies the [[anti-fabrication-protocol]] as a reusable procedure.

---

## TODO: Procedure (not yet written)

### Step 1: Identify the Claim
- [ ] What did the agent claim to create/modify/verify?
- [ ] What artifact or state change was asserted?
- [ ] Is this a fabrication-risk claim? (See [[anti-fabrication-protocol]])

### Step 2: Select Verification Method

| Claim Type | Verification Method |
|-----------|---------------------|
| File created/modified | `ls -la <path>` or `test -f <path>` |
| Config patched | `grep <pattern> <file>` |
| Database table/row created | `psql -c "SELECT..."` |
| Service restarted | `curl <health-endpoint>` or `systemctl status` |
| Secret updated | Vault query (never grep secrets directly) |
| Network accessible | `curl -s -o /dev/null -w "%{http_code}" <url>` |
| Docker container running | `docker ps | grep <name>` |

### Step 3: Execute Verification
- [ ] Run the appropriate verification command
- [ ] Capture output
- [ ] Compare output against expected state

### Step 4: Report Result

**If verification PASSES:**
- [ ] Report success with evidence (include verification command + output)
- [ ] Log to VAULT999 if HIGH risk_band

**If verification FAILS:**
- [ ] Report actual state (not claimed state)
- [ ] Do not claim success if verification failed
- [ ] File scar if this represents a new failure mode
- [ ] Log to VAULT999

### Step 5: Anti-Fabrication Checklist (before closing)

- [ ] File exists? → `ls` confirmed
- [ ] Config patched? → `grep` confirmed
- [ ] Database updated? → `psql SELECT` confirmed
- [ ] Service healthy? → health endpoint confirmed
- [ ] Secret accessible? → vault query confirmed

---

## Preconditions

- Terminal access or API access to the system being verified
- Vault access (for secret verification)
- Appropriate read permissions on target files/DBs

---

## Expected Outputs

- Verification command output captured
- Result reported based on evidence (not confidence)
- VAULT999 outcome logged (for HIGH risk_band)
- Log entry in `AAA/wiki/log.md`

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Verification command fails (not found) | Try alternative verification method |
| Permission denied | Escalate; do not claim success without evidence |
| Race condition (file deleted after check) | Retry once; report actual state if still failing |
| Service health check returns unexpected code | Report actual code; do not claim healthy |
| DB query returns empty | Empty ≠ doesn't exist; verify with `COUNT(*)` not `SELECT *` |

---

## Relationship to Anti-Fabrication Protocol

This skill is the **operational procedure** derived from the [[anti-fabrication-protocol]] concept page.

- **Concept page** (`anti-fabrication-protocol.md`): Defines the principle — verify before claiming
- **This skill** (`skill-evidence-verification.md`): Specifies the exact procedure for doing it

The concept page is the "why." This skill is the "how."

---

## Related Pages

- [[anti-fabrication-protocol]] — the concept (why verification is required)
- [[scar-hermes-fabrication-2026-05-17]] — the incident that drove this skill
- [[skill-spatial-grounding]] — first skill that used this protocol in practice

---

## Stub Author Notes

This skill generalizes the verification procedure already embedded in [[skill-spatial-grounding.md]] (Step 3: Verify the patch) into a standalone, reusable skill.

**Next step:** Extract the verification patterns from skill-spatial-grounding and from the scar's verification commands to build the table in Step 2.

*DITEMPA BUKAN DIBERI — Evidence before claim. Always.*
