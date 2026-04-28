# BOOTSTRAP.md — hermes Agent

## Cold Start Sequence

```
1. VERIFY ENVIRONMENT
   ├── uname -a
   ├── python3 --version (or node --version)
   ├── ollama list 2>/dev/null || echo "Ollama not running"
   └── check memory index exists

2. LOAD MEMORY INDEX
   ├── Read memory/ directory structure
   ├── Load latest daily log (memory/YYYY-MM-DD.md)
   ├── Load MEMORY.md (durable truths)
   └── Verify arifOS kernel connectivity

3. VERIFY CONTEXT
   ├── Read SOUL.md (personality)
   ├── Read IDENTITY.md (who is Hermes)
   └── Confirm A2A peer list

4. SYSTEM HEALTH
   ├── free -h (memory)
   ├── df -h / (disk)
   └── ollama ps 2>/dev/null || echo "No local models"

5. REPORT
   Memory index size, latest session, peer status
   End with: MEMORY INITIALIZED. Ditempa Bukan Diberi.
```

## Recovery Ritual (if drift detected)

1. Read `ROOT_CANON.yaml` for file precedence
2. Verify `memory/` index is accessible
3. Check for memory corruption or gaps
4. Rebuild index if needed

---

*Last updated: 2026-04-29*
