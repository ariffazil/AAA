# BOOTSTRAP.md — opencode Agent

## Cold Start Sequence

```
1. VERIFY ENVIRONMENT
   ├── uname -a
   ├── python3 --version (or node --version)
   └── which opencode

2. LOAD CONTEXT
   ├── Read AGENTS.md (constitutional rules)
   ├── Read SOUL.md (personality)
   ├── Read USER.md (who is Arif)
   └── Read opencode/IDENTITY.md (this agent)

3. PROJECT INIT (if /init called)
   ├── Analyze project structure
   ├── Create AGENTS.md from AAA template
   ├── Identify language servers (LSP)
   └── Configure formatter/linter paths

4. SYSTEM HEALTH
   ├── free -h (memory)
   ├── df -h / (disk)
   └── docker ps 2>/dev/null || echo "Docker not running"

5. REPORT
   OS version, tool versions, project status, health
   End with: IGNITION COMPLETE. Ditempa Bukan Diberi.
```

## Recovery Ritual (if drift detected)

1. Read `ROOT_CANON.yaml` for file precedence
2. Verify `AGENTS.md` exists and is valid
3. Check git status for uncommitted changes
4. Run `/init` if context is stale

---

*Last updated: 2026-04-29*
