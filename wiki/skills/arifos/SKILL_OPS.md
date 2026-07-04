---
title: "SKILL: VAULT999 Operations"
type: skill
version: 1.0.0
category: governance
risk_band: HIGH
floors: [F1, F2, F3, F13]
evidence_required: true
sources: [/root/.opencode/skills/vault999-ops/SKILL.md]
confidence: high
---

# SKILL: VAULT999 Operations

> **DITEMPA BUKAN DIBERI — VAULT999 is append-only. Not a secret store.**
> **Source:** `/root/.opencode/skills/vault999-ops/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Reading, verifying, merging, or auditing VAULT999 data
- Writing to outcomes.jsonl
- Checking vault integrity
- Chain verification
- Keywords: VAULT999, vault, outcomes.jsonl, SEALED_EVENTS, ledger, audit, Merkle

---

## What VAULT999 IS and IS NOT

| IS | IS NOT |
|----|--------|
| Append-only audit ledger | ❌ Secret/credential store |
| Immutable chain of evidence | ❌ Database for queries |
| Hash-chained (Merkle) records | ❌ General-purpose key-value store |
| Archived verdicts & tool calls | ❌ API keys storage |

---

## Physical Architecture (2026-05-14 — Unified)

```
CANONICAL (live): /root/.local/share/arifos/vault999/outcomes.jsonl (2171 lines)
                 ↑ symlink /root/VAULT999 → this directory
                 ↑ append-only flag (chattr +a) is SET

DEPRECATED:      /var/lib/arifos/vault/outcomes.jsonl.DEPRECATED
DEPRECATED:      /var/lib/arifos/volumes/vault999/outcomes.jsonl.DEPRECATED
SNAPSHOT:        /root/arifOS/VAULT999/outcomes.jsonl (git-tracked, 9561 lines)

PostgreSQL:      docker exec postgres psql -U arifos_admin -d vault999 -c "SELECT count(*) FROM vault_seals;"
vault999 API:    http://localhost:8100/health
vault999-writer: http://localhost:5001/health
```

---

## Safe Operations

### Read (Always Safe)
```bash
tail -20 /root/.local/share/arifos/vault999/outcomes.jsonl
wc -l /root/.local/share/arifos/vault999/outcomes.jsonl
grep "TOOL_CALL" /root/.local/share/arifos/vault999/outcomes.jsonl | tail -5
```

---

## Write (Requires F1 Amanah Check)

The file has `chattr +a` (append-only). To write:

```bash
# 1. Remove append-only flag (requires root)
chattr -a /root/.local/share/arifos/vault999/outcomes.jsonl

# 2. Write safely (always append, never truncate)
echo '{"ts": "...", "event": "..."}' >> /root/.local/share/arifos/vault999/outcomes.jsonl

# 3. Restore append-only flag
chattr +a /root/.local/share/arifos/vault999/outcomes.jsonl
```

---

## Merge (Requires 888_HOLD)

1. Backup current canonical file FIRST
2. Read all copies, deduplicate by (ts + event_id + content hash)
3. Write merged to temp file
4. chattr -a, replace, chattr +a
5. Mark stale copies as .DEPRECATED, never delete

---

## Verify Integrity

```bash
# Check append-only flag
lsattr /root/.local/share/arifos/vault999/outcomes.jsonl
# Should show: -----a--------e-------

# Verify symlink
readlink -f /root/VAULT999
# Should return: /root/.local/share/arifos/vault999
```

---

## Health Check

```bash
curl http://localhost:8100/health
# Expected: {"status": "healthy", "sealed": 4, "holding": 0}
```

---

## Related Pages

- [[skill-vault-integrity]] — vault integrity reasoning
- [[skill-constitutional-reasoning]] — F1/F2/F3 reasoning
- [[concept-memory-knowledge-loop]] — memory as sealed trace
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Vault append-only. Integrity verified.*
