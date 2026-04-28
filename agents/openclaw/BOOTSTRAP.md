# BOOTSTRAP.md — openclaw Agent

## Cold Start Sequence

```
1. VERIFY ENVIRONMENT
   ├── uname -a
   ├── docker ps (verify containers running)
   ├── openclaw status 2>/dev/null || echo "OpenClaw not running"
   └── check channel connections

2. LOAD CONTEXT
   ├── Read AGENTS.md (constitutional rules)
   ├── Read SOUL.md (personality)
   ├── Read USER.md (who is Arif)
   ├── Read IDENTITY.md (this agent)
   └── Verify peer agents accessible

3. VERIFY GATEWAY CONFIG
   ├── Check openclaw/gateway/default.yaml
   ├── Verify channel tokens via SecretRef
   └── Verify A2A peers registered

4. SYSTEM HEALTH
   ├── docker ps (all containers healthy)
   ├── free -h (memory)
   ├── df -h / (disk)
   └── peer connectivity test

5. REPORT
   Gateway status, channel status, peer status
   End with: GATEWAY ONLINE. Ditempa Bukan Diberi.
```

## Recovery Ritual (if drift detected)

1. Verify all channel connections
2. Test A2A peer connectivity
3. Check VAULT999 connectivity
4. Review recent audit events

---

*Last updated: 2026-04-29*
