# BOOTSTRAP.md — hermes-ops Agent

## Cold Start Sequence

```
1. VERIFY ENVIRONMENT
   ├── uname -a
   ├── docker available?
   ├── git configured?
   └── ci/cd pipelines accessible?

2. LOAD CANON (in order)
   ├── SOUL.md
   ├── USER.md
   ├── IDENTITY.md
   ├── AGENTS.md
   ├── arifos.init
   └── MEMORY.md

3. VERIFY TOOLS
   ├── claude-code functional?
   ├── github-pro connected?
   ├── arifos-deploy ready?
   └── docker containers accessible?

4. TEMPORAL ANCHOR
   ├── Check clock
   └── Set epoch_now

5. REPORT
   Agent status, tool status, Ω₀
   End with: OPS INITIALIZED. Ship it clean.
```

---

*Last updated: 2026-04-29*
