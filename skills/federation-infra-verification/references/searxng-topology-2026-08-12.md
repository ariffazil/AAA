# SearXNG Sovereign Search — Full Wiring Topology (2026-08-12)

> Session-specific reference. The general pattern lives in §13a of the skill SKILL.md.
> Verified by live probe 2026-08-12T05:01:52Z.

## Architecture

```
Layer Atas (Federated)  : Gemini 3.6 Flash + DashScope PAYG (model reasoning)
Layer Bawah (Owned)     : SearXNG :8080 (search), VAULT999 (truth), A-FORGE (execution)
Decoupling             : Search layer survives model layer outage
```

## The 7-Link Verification Chain

### Link 1: Docker process
```bash
ps aux | grep searxng | grep -v grep
# Expected: searxng + searxng worker-1 (pid 6213, started Jul 23)
```

### Link 2: Port binding
```bash
ss -tlnp | grep :8080
# Expected: docker-proxy on 127.0.0.1:8080
```

### Link 3: Functional endpoint
```bash
curl -s "http://localhost:8080/search?q=flanil&format=json" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f'results={len(d.get(\"results\",[]))} unresponsive={d.get(\"unresponsive_engines\",[])}')
"
# Expected: 20+ results, possibly 1 unresponsive engine (startpage CAPTCHA = normal)
```

### Link 4: Hermes global config
```bash
grep -A3 "web:" /root/.hermes/config.yaml
# Expected: backend: searxng / search_backend: searxng / extract_backend: searxng
```

### Link 5: Per-profile configs
```bash
for p in hermes-asi hermes_forge hermes_apex aaa-hermes; do
  echo "=== $p ==="
  cat /root/.hermes/profiles/$p/config.yaml 2>/dev/null | grep -E "backend|search_backend|extract_backend" | head -5
done
# Expected: hermes_forge + hermes_apex show search_backend: searxng
# aaa-hermes inherits global (no override)
```

### Link 6: A-FORGE code defaults
```bash
grep -n "localhost:8080\|searxngBase" /root/A-FORGE/src/interfaces/mcp/proxyTools.ts | head -5
# Expected: line 1129: const searxngBase = (params.searxng_url || params.url || "http://localhost:8080");
```

### Link 7: Environment + systemd
```bash
grep SEARXNG /root/.secrets/kunci-mas.env
# Expected: SEARXNG_URL=http://127.0.0.1:8080

grep SEARXNG /root/.secrets/kunci-mas.flat.env
# Expected: same (flat.env consumed by systemd)

systemctl show hermes-asi-gateway.service | grep EnvironmentFiles
# Expected: /root/.secrets/kunci-mas.flat.env
```

## Full chain verification script

```bash
#!/bin/bash
echo "=== SearXNG 7-Link Topology Verification ==="
echo -n "1. Process: "; ps aux | grep -c "[s]earxng" | xargs -I{} echo "{} processes"
echo -n "2. Port: "; ss -tlnp | grep -c ":8080" | xargs -I{} echo "{} listeners"
echo -n "3. Functional: "; curl -s "localhost:8080/search?q=test&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"results\",[]))} results')" 2>/dev/null || echo "FAIL"
echo -n "4. Global config: "; grep -c "searxng" /root/.hermes/config.yaml | xargs -I{} echo "{} matches"
echo -n "5. Profiles: "; grep -rl "searxng" /root/.hermes/profiles/*/config.yaml 2>/dev/null | wc -l | xargs -I{} echo "{} profiles"
echo -n "6. A-FORGE: "; grep -c "localhost:8080" /root/A-FORGE/src/interfaces/mcp/proxyTools.ts | xargs -I{} echo "{} references"
echo -n "7. Env: "; grep -c "SEARXNG_URL" /root/.secrets/kunci-mas.env | xargs -I{} echo "{} entries"
```

## What Was NOT Fixed (Open Issues from Same Session)

The "resolution report" claimed full fix but these ecosystem issues were silent:

| Issue | Evidence | Impact |
|---|---|---|
| Honcho memory plugin DOWN | `Connection refused [Errno 111]` recurring in agent.log | Cross-session dialectic memory broken |
| hound MCP server parked | JSONRPC parse errors, 3/3 retries failed | Search-related MCP tool unavailable |
| aforge MCP cyclic reconnect | `connection lost (attempt 1/5)` in logs | forge_fetch/forge_search may be intermittent |
| Event loop crashes | `RuntimeError: Event loop is closed` in mcp_tool.py:2783 | Cleanup race condition during MCP reconnect |

**Lesson:** "What I changed" ≠ "What's still broken." Always probe ancillary services.
