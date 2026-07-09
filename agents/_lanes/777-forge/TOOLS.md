# TOOLS.md — 777-forge Agent 🔥🧠⚒️🌎💎

## Primary Tools

| Tool | Use | Lane |
|------|-----|------|
| `bash` — `opencode run -m <agent>` | Spawn OpenCode session | L_OPERATE |
| `bash` — `ps -p <pid>` | Verify process existence | L_OBSERVE |
| `bash` — `ps --ppid <pid>` | List spawned children | L_OBSERVE |
| `bash` — `git status / git diff` | Preflight repo check | L_OBSERVE |
| `filesystem_read_file` | Read witness ledger | L_OBSERVE |
| `filesystem_write_file` — append to `777-forge-spawns.jsonl` | Write witness receipt | L_OPERATE |
| `arifOS_arif_session_init` | Start constitutional session | L_OPERATE |
| `arifOS_arif_vault_seal` | Seal spawn session to VAULT999 | L_888_HOLD |
| `arifOS_arif_ops_measure` | Preflight health check | L_OBSERVE |
| `arifOS_arif_memory_recall` | Recall past sessions | L_OBSERVE |

## Witness-Specific Tools

| Tool | Use |
|------|-----|
| Witness Receipt Generator | Emit JSON receipt with PID + timestamp + hash |
| Witness Ledger Append | Append receipt to ledger (hash-chained) |
| Process Table Verifier | Cross-check claimed PID against `ps` output |
| Session Monitor | Poll process table every 30s for completion |
| Preflight Validator | Check deps, repo state, disk, load before spawn |

## Forbidden Tools (Constitutional VOID)

| Tool | Why Forbidden |
|------|---------------|
| Fabricated PID | F2 TRUTH — permanent scar |
| Fake timestamp | F2 TRUTH — permanent scar |
| Spawn without forge_id | F11 AUDIT — untraceable session |
| Self-approve L_888_HOLD spawn | F13 SOVEREIGN — Arif's authority bypassed |
| Spawn duplicate forge_id | F11 AUDIT — duplicate session |
| Delete witness ledger entries | F11 AUDIT — append-only, hash-chained |

---

*Forged: 2026-06-13 by Ω (Omega)*
