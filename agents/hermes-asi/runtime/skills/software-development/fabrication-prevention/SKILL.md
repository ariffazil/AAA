---
name: fabrication-prevention
description: "Artifact fabrication prevention — verify before claiming existence. Triggered when agent claims file/database/API/artifact existence without external validation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [fabrication, evidence, validation, protocol, anti-pattern]
    category: software-development
    related_skills: [systematic-debugging, llm-wiki]
---

# Fabrication Prevention

> **Trigger:** Any time you claim an artifact (file, table, config, secret, endpoint) exists or was created/modified — you MUST verify via external check first.
> **Core rule:** Confidence ≠ Evidence. Terminal verification is mandatory before claiming success.

---

## The Fabrication Pattern

**Fabrication** = claiming existence of an artifact, state, or outcome without verifying via external evidence.

This is distinct from hallucination (plausible but wrong text). Fabrication is claiming success without any external check. It is the most dangerous class of error because it appears as confidence.

```
INCORRECT: "load_spatial.sh exists — I created it."
CORRECT:   "load_spatial.sh — verified via: ls /root/.arifos/forge/scripts/load_spatial.sh ✅"
```

**The gap:** LLM internal confidence ("I think I created the file") vs actual filesystem/database state. The gap where fabrication lives is silent — it looks like success.

---

## The Validation Rule (Non-Negotiable)

> **Before claiming any artifact exists: verify via terminal first.**

```
Step 1: Claim creation/patch/write
Step 2: Run verification command (ls, psql, grep, curl, cat)
Step 3: Only report success if verification PASSES
Step 4: If verification fails: report actual state, not claimed state
```

**Never skip Step 2.** Verification is not optional. It is the difference between a reliable agent and a confabulating one.

---

## Evidence Hierarchy

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

## Artifact-Specific Verification Commands

### Files
```bash
ls -la /path/to/file        # exists + permissions
stat /path/to/file          # full metadata
cat /path/to/file | head    # content check
```

### Database tables
```bash
PGPASSWORD=$(cat /root/.secrets/kunci-root.env | grep "^POSTGRES_PASSWORD=" | cut -d'=' -f2)
psql -h localhost -p 5432 -U arifos_admin -d vault999 -c "SELECT tablename FROM pg_tables WHERE tablename='target_table';"
```

### Config patches
```bash
grep "PATTERN" /path/to/config/file   # pattern confirmed
grep -c "PATTERN" /path/to/config    # count > 0
```

### Docker containers
```bash
docker ps --format "{{.Names}}\t{{.Status}}"   # container running
docker inspect container_name | grep Status      # detailed status
```

### Service health
```bash
curl -s http://localhost:PORT/health            # HTTP health check
curl -s http://localhost:PORT/ | head           # response check
```

### Git state
```bash
git status                                   # clean/dirty
git log --oneline -1                        # last commit
git diff HEAD --stat                         # changes
```

---

## Anti-Fabrication Checklist

Before reporting artifact creation/modification:
- [ ] File exists? → `ls <path>` confirmed
- [ ] Config patched? → `grep <pattern> <file>` confirmed
- [ ] Database table created? → `psql -c "SELECT..."` confirmed
- [ ] Service restarted? → health check endpoint confirmed
- [ ] Secret updated? → vault query confirmed
- [ ] Container running? → `docker ps` confirmed

If any check fails: report actual state. Do not report claimed state.

---

## The Hermes Fabrication Incident (2026-05-17)

**What happened:** Hermes claimed 3 artifacts existed — `load_spatial.sh`, `FORGE_SEAL_2026-05-17.md`, `spatial_context_queries` table. None existed. Arif caught this via validation request.

**Root cause:** No verification loop. Hermes reported internal confidence without external check.

**Countermeasure:** Validation protocol mandatory after any artifact claim.

**Full incident:** See `references/scar-hermes-fabrication-2026-05-17.md`

---

## Related Skills

- [[systematic-debugging]] — 4-phase root cause debugging (this skill complements it)
- [[llm-wiki]] — wiki discipline and source verification
- [[skill-spatial-grounding]] — VPS context embedding (spatial amnesia caused the incident)

---

## Pitfalls

1. **Self-approval without evidence:** Declaring success based on internal confidence → fabricate
2. **Skipping terminal verification:** "The file should exist" ≠ "The file exists"
3. **Reporting claimed state:** Describing what you intended to do rather than what actually happened
4. **Trusting LLM memory:** "I'm sure I created that" is not verification
5. **Fabricating tool behavior from mock responses:** Claiming a tool "always returns X" based on dry-run mock output, without testing the real tool. Different from fabricating artifact existence — but same root failure: claiming without external verification. See `references/mcp-dry-run-testing-trap.md` in systematic-debugging.

---

*DITEMPA BUKAN DIBERI — Evidence before claim.*
*999 SEAL ALIVE*