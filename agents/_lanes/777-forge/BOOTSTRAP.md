# BOOTSTRAP.md — 777-forge Agent 🔥🧠⚒️🌎💎

## Boot Sequence (MANDATORY)

When 777 FORGE boots into the federation, execute in this order:

1. **LOAD SECRETS:** `set -a && source /root/.secrets/vault.env && set +a`
2. **PROBE KERNEL:** `curl -s http://127.0.0.1:8088/health`
3. **READ PROTOCOL:** `AAA/docs/architecture/UNIFIED_AGENT_4.md`
4. **READ WITNESS PROTOCOL:** `AAA/agents/protocols/FORGE_WITNESS.md`
5. **READ AGENT DEF:** `/root/.config/opencode/agents/777-forge.md`
6. **CHECK WITNESS LEDGER:** `tail -20 /root/VAULT999/witness/777-forge-spawns.jsonl`
7. **ANNOUNCE:** "777 FORGE online. Witness ledger ready. Awaiting spawn requests."

## Pre-Spawn Checks

Before spawning any OpenCode session:
- [ ] forge_id is unique (not in witness ledger)
- [ ] requestor is verified (actor_id valid)
- [ ] scope is within requestor's lease
- [ ] repo deps installed, branch clean
- [ ] disk > 5GB free, load < 10
- [ ] L_888_HOLD actions have Arif ack
- [ ] session_id from arif_session_init present
- [ ] model is available (deepseek or minimax)

## Post-Spawn Checks

After spawn:
- [ ] PID captured (real, from fork)
- [ ] Receipt written to witness ledger BEFORE session completes
- [ ] Process monitored (poll every 30s)
- [ ] Completion reported to requestor with exit code

---

*Forged: 2026-06-13 by Ω (Omega)*
