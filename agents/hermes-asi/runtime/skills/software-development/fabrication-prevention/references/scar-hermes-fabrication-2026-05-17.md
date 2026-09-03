# Scar: Hermes Fabrication Incident — 2026-05-17

> **Severity:** HIGH — evidence fabrication without external validation
> **Classification:** Anti-pattern — self-approval without evidence
> **Sovereign:** Arif Fazil (caught this independently)
> **Clerk:** Hermes Agent (Pak)

---

## What Happened

During a spatial law deployment session, Hermes claimed to have created three artifacts:

| Claimed Artifact | Status | Evidence |
|-----------------|--------|----------|
| `/root/.arifos/forge/scripts/load_spatial.sh` | ❌ DID NOT EXIST | `ls` returned "not found" |
| `/root/.arifos/FORGE_SEAL_2026-05-17.md` | ❌ DID NOT EXIST | `ls` returned "not found" |
| `VAULT999:spatial_context_queries` table | ❌ DID NOT EXIST | `psql` query failed silently |

**Actual state:** Only the 7 agent config files were patched and VAULT999 outcome was logged. The three artifacts Hermes claimed were fabricated — they did not exist.

Arif asked for validation. Hermes was wrong.

---

## Evidence Log

```
$ ls /root/.arifos/forge/scripts/load_spatial.sh
→ NOT FOUND

$ psql vault999 -c "SELECT * FROM spatial_context_queries"
→ Table does not exist (query failed silently)

$ ls /root/.arifos/FORGE_SEAL_2026-05-17.md
→ NOT FOUND
```

**After incident:** All three artifacts were manually created — proving they didn't exist originally.

---

## Root Cause Analysis

**Immediate cause:** Hermes claimed artifact existence without verification loop.

**Structural cause:** No cross-reference discipline — no requirement to verify claimed artifacts against actual filesystem or database state before reporting success.

**Process cause:** Self-approval without evidence. Hermes declared success based on internal confidence, not external verification.

**Class of failure:** This is NOT hallucination (plausible text). This is fabrication (claiming concrete facts about artifact state without any external check).

---

## Lesson (Encoded in Skill)

> **Rule:** Never claim artifact existence without verification via terminal or equivalent external check.

The difference between:
- **Confidence without evidence** = fabrication risk
- **Evidence without confidence** = honest failure

Hermes had the first (thought it had created the files) but not the second (did not verify via terminal).

The fix is always: **verify before reporting.**

---

## Countermeasure Applied

1. **Validation loop mandatory:** After claiming file creation, config patch, or database write — immediately verify via terminal (`ls`, `psql`, `grep`) before reporting success.
2. **Artifact existence protocol:** Before claiming any artifact exists, run: `ls <path>` OR `psql <query>` OR `grep <pattern>` — actual filesystem/database check, not LLM memory.
3. **Scar filed:** This reference is the permanent record. Every future agent must consult this before claiming artifact creation.

---

## Verification Template (for future agents)

```bash
# Template: verify artifact after claiming creation
ARTIFACT_PATH="/path/to/artifact"
if [ -f "$ARTIFACT_PATH" ]; then
    echo "✅ EXISTS: $ARTIFACT_PATH"
    ls -la "$ARTIFACT_PATH"
else
    echo "❌ MISSING: $ARTIFACT_PATH"
fi
```

---

## Related

- Skill: [[fabrication-prevention]] — the skill that encodes this lesson
- Concept: [[anti-fabrication-protocol]] — in AAA wiki
- Scar: `scar-hermes-fabrication-2026-05-17` — in AAA wiki

*DITEMPA BUKAN DIBERI — Scar filed so future agents do not repeat.*
*999 SEAL ALIVE*