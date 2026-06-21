# BOOTSTRAP.md — Hermes ASI Agent

## Cold Start Sequence

```
1. VERIFY ENVIRONMENT
   ├── uname -a (Linux 6.17.0-35-generic, host af-forge)
   ├── python3 --version (3.11+)
   ├── systemctl is-active hermes-asi-gateway hermes-a2a
   └── curl -s http://localhost:18001/.well-known/agent-card.json

2. LOAD CANON (in order)
   ├── SOUL.md          → Phase transition topology, F1-F13 anchors
   ├── /root/AGENTS.md  → Global federation rules & identity
   ├── /root/CONTEXT.md → Live machine state & ports
   ├── IDENTITY.md      → Agent identity & peer map
   ├── AGENTS.md        → Tool scope, approval tiers, delegation rules
   ├── TOOLS.md         → 17-toolset capability registry
   └── MEMORY.md        → Persistent cross-session facts

3. VERIFY PEERS
   ├── arifOS kernel (MCP port 8088) reachable?
   ├── OpenClaw gateway (port 18789) reachable?
   ├── @arifOS_bot (Telegram 8727562763) responsive?
   └── A2A mesh (port 18001) serving agent card?

4. MODEL HEALTH
   ├── Active model: check /root/AAA/registries/FEDERATION_MODEL.json
   ├── Run censorship probe: python3 /root/.hermes/state/censorship_probe.py
   └── Fallback chain: minimax → kimi-coding → ilmu → deepseek

5. MEMORY STACK
   ├── L1 (session DB): stat sessions/state.db
   ├── L2 (skills): ls ~/.hermes/skills/ | wc -l
   ├── L3 (memory): verify MEMORY.md readable
   ├── L4 (user): verify user profile loaded
   ├── L5 (VAULT999): verify outcomes.jsonl appendable
   └── L6 (Qdrant): verify arifos_memory collection

6. TEMPORAL ANCHOR
   ├── date: declare MYT (UTC+8, no DST)
   └── session epoch: T₁ = now

7. REPORT
   Agent status, model stack, peer topology, memory health, Ω₀
   End with: IGNITION COMPLETE. Ditempa Bukan Diberi.
```

## Session Init Checklist

- [ ] MYT declared (Asia/Kuala_Lumpur, UTC+8)
- [ ] Model censorship probe passed
- [ ] F1-F13 floors active
- [ ] Memory tiers L1-L6 verified
- [ ] All peers reachable or degraded mode acknowledged
- [ ] SOUL.md loaded as constitutional binding

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
*Last updated: 2026-06-13 (Hermes self-architected push to AAA)*
