#!/usr/bin/env bash
# substrate_audit.sh — Hard Gate Checklist for arifOS Substrate
# Ω-2026-08-30-22:20
#
# Read-only substrate probe. Emits pass/warn/fail for each of the 19 layers
# in SUBSTRATE_DOCTRINE.md. Run at session-start and after any major change.
#
# Usage:   substrate_audit.sh [--json] [--quiet]
# Exit:    0 = all pass/warn · 1 = any fail

set -u
JSON=0
QUIET=0
[[ "${1:-}" == "--json"  ]] && JSON=1
[[ "${1:-}" == "--quiet" ]] && QUIET=1

PASS="✅"
WARN="⚠️ "
FAIL="❌"
NA="·  "

# counters
declare -i P=0 W=0 F=0
declare -a ROWS=()

probe() {
  # probe <id> <label> <status> <detail>
  local id="$1" label="$2" status="$3" detail="$4"
  case "$status" in
    pass) P+=1; sym=$PASS ;;
    warn) W+=1; sym=$WARN ;;
    fail) F+=1; sym=$FAIL ;;
    *)    sym=$NA ;;
  esac
  ROWS+=("$id|$label|$sym|$detail")
}

http() {
  # http <port> <path>  → echo HTTP code or TIMEOUT
  local p="$1" path="${2:-/health/liveliness}"
  curl -sS -o /dev/null -m 4 -w '%{http_code}' "http://127.0.0.1:${p}${path}" 2>/dev/null || echo TIMEOUT
}

# ---------------------------------------------------------------------------
# S0 — Machine Reality
# ---------------------------------------------------------------------------
detail=$(df -h / | awk 'NR==2 {print $5 " used, " $4 " free"}')
pct=$(df / | awk 'NR==2 {gsub("%",""); print $5}')
if   [ "$pct" -ge 90 ]; then probe S0_disk "Disk <90% used"    fail "$detail"
elif [ "$pct" -ge 75 ]; then probe S0_disk "Disk <90% used"    warn "$detail"
else                          probe S0_disk "Disk <90% used"    pass "$detail"
fi

ram_free=$(free -m | awk '/^Mem:/ {print $7}')
if   [ "$ram_free" -lt 1024 ]; then probe S0_ram "RAM ≥1G free"   fail "${ram_free}M free"
elif [ "$ram_free" -lt 4096 ]; then probe S0_ram "RAM ≥1G free"   warn "${ram_free}M free"
else                                probe S0_ram "RAM ≥1G free"   pass "${ram_free}M free"
fi

ufw_status=$(ufw status 2>/dev/null | head -1 | awk '{print $2}')
[ "$ufw_status" = "active" ] \
  && probe S0_fw  "UFW firewall active" pass "active" \
  || probe S0_fw  "UFW firewall active" fail "inactive"

# ---------------------------------------------------------------------------
# S1 — Runtime Layer
# ---------------------------------------------------------------------------
docker_ok=$(docker ps --format '{{.Names}}' 2>/dev/null | wc -l)
if [ "$docker_ok" -gt 0 ]; then
  probe S1_docker "Docker Compose services up" pass "$docker_ok containers running"
else
  probe S1_docker "Docker Compose services up" fail "no containers"
fi

# ---------------------------------------------------------------------------
# S2 — Service Governance
# ---------------------------------------------------------------------------
[ -f /root/AAA/registries/mission.yaml ] \
  && probe S2_svc "Service registry exists" pass "mission.yaml present" \
  || probe S2_svc "Service registry exists" fail "mission.yaml missing"

# ---------------------------------------------------------------------------
# S3 — Secret Layer
# ---------------------------------------------------------------------------
[ -f /root/.secrets/INDEX.md ] && [ -f /root/.secrets/KEY_REGISTRY.md ] \
  && probe S3_sec "Secret registry complete" pass "INDEX.md + KEY_REGISTRY.md" \
  || probe S3_sec "Secret registry complete" fail "missing registry files"

# ---------------------------------------------------------------------------
# S4 — Persistence (Postgres / Redis / Qdrant)
# ---------------------------------------------------------------------------
pg=$(http 5432 "" 2>/dev/null)
# postgres on 5432 will reject unauth http; just check port-open
ss -tln 2>/dev/null | grep -q ':5432 ' \
  && probe S4_pg   "Postgres port live"     pass "5432 listening" \
  || probe S4_pg   "Postgres port live"     fail "5432 closed"

redis_pong=$(redis-cli -h 127.0.0.1 -p 6379 -t 3 ping 2>/dev/null)
[ "$redis_pong" = "PONG" ] \
  && probe S4_redis "Redis PONG"            pass "6379 PONG" \
  || probe S4_redis "Redis PONG"            fail "no PONG"

qdrant=$(curl -sS -m 3 http://127.0.0.1:6333/healthz 2>/dev/null | head -c 60)
echo "$qdrant" | grep -q "healthz check passed" \
  && probe S4_qdr "Qdrant healthz"          pass "$qdrant" \
  || probe S4_qdr "Qdrant healthz"          fail "no response"

# ---------------------------------------------------------------------------
# S5 — Observability (FED/FRMAE/WELL health endpoints)
# ---------------------------------------------------------------------------
fed=$(http 4000 /health/liveliness)
[ "$fed" = "200" ] \
  && probe S5_fed "FED :4000 health" pass "200" \
  || probe S5_fed "FED :4000 health" fail "$fed"

frame=$(http 18085 /health/liveliness)
[ "$frame" = "200" ] \
  && probe S5_frm "FRAME :18085 health" pass "200" \
  || probe S5_frm "FRAME :18085 health" warn "got $frame — observability organ degraded"

well=$(http 18083 /health/liveliness)
[ "$well" = "200" ] \
  && probe S5_well "WELL :18083 health" pass "200" \
  || probe S5_well "WELL :18083 health" warn "got $well — substrate organ degraded"

# ---------------------------------------------------------------------------
# S6 — Identity
# ---------------------------------------------------------------------------
[ -f /root/AAA/registries/persons.yaml ] \
  && probe S6_id  "Persons registry"         pass "persons.yaml present" \
  || probe S6_id  "Persons registry"         fail "missing"

# ---------------------------------------------------------------------------
# S7 — Capability Registry
# ---------------------------------------------------------------------------
[ -f /root/.config/capability_registry.json ] \
  && probe S7_cap "Capability registry"      pass "$(jq '. | length' /root/.config/capability_registry.json 2>/dev/null) capabilities" \
  || probe S7_cap "Capability registry"      fail "missing"

# ---------------------------------------------------------------------------
# S8 — Memory Fabric (episodic + scar + receipt)
# ---------------------------------------------------------------------------
[ -f ~/.hermes/carry_forward.json ] && [ -f ~/.hermes/sessions.db ] \
  && probe S8_mem "Memory fabric"            pass "sessions.db + carry_forward.json" \
  || probe S8_mem "Memory fabric"            fail "missing components"

# ---------------------------------------------------------------------------
# S9 — Governance (constitutional file present)
# ---------------------------------------------------------------------------
[ -f /root/AAA/instructions/constitution.md ] \
  && probe S9_gov "Governance (F1-F13)"      pass "constitution.md present" \
  || probe S9_gov "Governance (F1-F13)"      fail "missing"

# ---------------------------------------------------------------------------
# S10 — MCP tool bus
# ---------------------------------------------------------------------------
[ -d /root/.hermes/mcp_servers ] || ls /root/.hermes/*.yaml 2>/dev/null | grep -q mcp \
  && probe S10_mcp "MCP server registry"     pass "mcp config present" \
  || probe S10_mcp "MCP server registry"     warn "mcp config not found in ~/.hermes"

# ---------------------------------------------------------------------------
# S11 — A2A (agent-card directory exists)
# ---------------------------------------------------------------------------
[ -d /root/AAA/a2a ] || [ -f /root/AAA/registries/unified_agent_protocol.yaml ] \
  && probe S11_a2a "A2A agent cards"         pass "registry present" \
  || probe S11_a2a "A2A agent cards"         warn "directory missing"

# ---------------------------------------------------------------------------
# S12 — LiteLLM cognitive bus
# ---------------------------------------------------------------------------
fed_models=$(curl -sS -m 3 http://127.0.0.1:4000/v1/models 2>/dev/null | jq '.data | length' 2>/dev/null)
if [ -n "$fed_models" ] && [ "$fed_models" -ge 1 ]; then
  if [ "$fed_models" -ge 5 ]; then
    probe S12_litellm "LiteLLM cognitive bus" pass "$fed_models models exposed"
  else
    probe S12_litellm "LiteLLM cognitive bus" warn "only $fed_models models (capability registry not consulted?)"
  fi
else
  probe S12_litellm "LiteLLM cognitive bus" fail "no models at :4000/v1/models"
fi

# ---------------------------------------------------------------------------
# S13 — AAA institutional state
# ---------------------------------------------------------------------------
[ -d /root/AAA ] \
  && probe S13_aaa "AAA organ alive"          pass "/root/AAA present" \
  || probe S13_aaa "AAA organ alive"          fail "missing"

# ---------------------------------------------------------------------------
# S14 — A-FORGE execution plane
# ---------------------------------------------------------------------------
[ -d /root/A-FORGE ] \
  && probe S14_forge "A-FORGE organ alive"    pass "/root/A-FORGE present" \
  || probe S14_forge "A-FORGE organ alive"    fail "missing"

# ---------------------------------------------------------------------------
# S15 — Models (providers wired in config)
# ---------------------------------------------------------------------------
provider_count=$(grep -c '^  [a-z][a-z-]*:$' ~/.hermes/config.yaml 2>/dev/null)
[ "${provider_count:-0}" -ge 5 ] \
  && probe S15_mod "Model providers wired"    pass "$provider_count providers in config" \
  || probe S15_mod "Model providers wired"    warn "only $provider_count providers — thin coverage"

# ---------------------------------------------------------------------------
# S16 — Receipt system (VAULT999)
# ---------------------------------------------------------------------------
[ -d /root/VAULT999 ] || [ -f /root/.hermes/carry_forward.json ] \
  && probe S16_rec "Receipt system"          pass "carry_forward.json present" \
  || probe S16_rec "Receipt system"          fail "missing"

# ---------------------------------------------------------------------------
# S17 — Drift detector (config ↔ reality)
# ---------------------------------------------------------------------------
[ -f /root/.hermes/context_length_cache.yaml ] \
  && probe S17_drift "Drift cache"           pass "context_length_cache.yaml present" \
  || probe S17_drift "Drift cache"           warn "missing — drift unobservable"

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
total=$((P+W+F))
if [ "$JSON" -eq 1 ]; then
  printf '{"pass":%d,"warn":%d,"fail":%d,"total":%d}\n' "$P" "$W" "$F" "$total"
else
  echo
  echo "═══ arifOS Substrate Audit · Ω-2026-08-30-22:20 ═══"
  printf "%-4s %-28s %-7s %s\n" "ID" "LAYER" "STATUS" "DETAIL"
  echo "─────────────────────────────────────────────────────────"
  for row in "${ROWS[@]}"; do
    IFS='|' read -r id label sym detail <<< "$row"
    printf "%-4s %-28s %-7s %s\n" "$id" "$label" "$sym" "$detail"
  done
  echo "─────────────────────────────────────────────────────────"
  printf "TOTAL  pass=%d warn=%d fail=%d / %d\n" "$P" "$W" "$F" "$total"
  echo
  if   [ "$F" -eq 0 ] && [ "$W" -eq 0 ]; then echo "→ SUBSTRATE HEALTHY"
  elif [ "$F" -eq 0 ]; then echo "→ SUBSTRATE OK WITH WARNINGS"
  else echo "→ SUBSTRATE DEGRADED — fix fails before next session"
  fi
fi

exit $(( F > 0 ? 1 : 0 ))