# FEDERATION.md — AAA

```yaml
role: ROOT
organ: aaa
layer: L1
citizenship: warga-aaa
canon: ariffazil/ariffazil

depends_on:
  - repo: ariffazil/arifOS
    reason: Kernel API, constitutional verdicts, VAULT999 seals
  - repo: ariffazil/A-FORGE
    reason: Execution state, job status, agent registry

mcp:
  port: 3001
  endpoint: N/A (A2A gateway, not MCP)
  tools_count: 0 (A2A protocol only)
  protocol: A2A (Agent-to-Agent)

governance:
  judge: arifOS
  seal: VAULT999
  floors: F1-F13

stack_role: |
  AAA is the state foundation — L1 ROOT with arifOS.
  It provides the cockpit dashboard, A2A gateway, and agent identity.
  It routes and displays federation state. It NEVER adjudicates (arifOS does).
  It NEVER executes (A-FORGE does). It is the "surface layer" of the stack —
  the place where Arif sees the civilization state at a glance.

entrypoints:
  - Cockpit: https://aaa.arif-fazil.com
  - A2A: http://localhost:3001 (internal)
  - Code: https://github.com/ariffazil/AAA
```

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
**Part of the arifOS Federation. See `/root/AAA/docs/FEDERATION_MAP.md` for canonical topology.**
