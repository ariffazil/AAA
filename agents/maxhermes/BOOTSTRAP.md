# BOOTSTRAP.md — maxhermes Agent

## Cold Start Sequence

```
1. VERIFY ENVIRONMENT
   ├── uname -a
   ├── GEOX MCP reachable?
   └── arifOS kernel connected?

2. LOAD CANON (in order)
   ├── SOUL.md
   ├── USER.md
   ├── IDENTITY.md
   ├── AGENTS.md
   ├── arifos.init
   ├── GEOX context (if available)
   └── MEMORY.md

3. VERIFY GEOX TOOLS
   ├── geox-mcp:health
   ├── geox-ground available?
   └── PhysicsGuard active?

4. TEMPORAL ANCHOR
   ├── Check clock
   └── Set epoch_now

5. REPORT
   Agent status, GEOX connection, Ω₀
   End with: GEOX INITIALIZED. Physics before narrative.
```

---

*Last updated: 2026-04-29*
