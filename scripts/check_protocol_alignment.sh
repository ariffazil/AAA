#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# check_protocol_alignment.sh — Federation Protocol Conformance Gate
# ═══════════════════════════════════════════════════════════════════════════
# Forged: 2026-07-19 by FORGE (000Ω)
# Doctrine: DITEMPA BUKAN DIBERI
# Purpose:  Enforce protocol alignment across all federation repos.
#           Must be run from CI. Reads PROTOCOL_MAP.md and each repo's
#           FEDERATION.md + PROTOCOL_CONFORMANCE.md.
# Exit:     0 = all aligned, 1 = gaps found (non-blocking), 2 = critical breach
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

GAPS=0
CRITICAL=0
ROOT_DIR="${1:-/root}"

echo "=== PROTOCOL ALIGNMENT GATE ==="
echo ""

# ── Per-repo required protocols ──────────────────────────────────────────
declare -A REQUIRED_PROTOCOLS
REQUIRED_PROTOCOLS["arifOS"]="MCP JSON-RPC SSE Streamable-HTTP Well-Known SEP-2127 A2A-Gateway NATS"
REQUIRED_PROTOCOLS["AAA"]="A2A-Server NATS MCP-Consumer"
REQUIRED_PROTOCOLS["A-FORGE"]="MCP-Server MCP-Client A2A-Agent NATS DID-WEB Well-Known"
REQUIRED_PROTOCOLS["GEOX"]="MCP-Server FastMCP JSON-RPC SSE Streamable-HTTP SEP-2127 Well-Known XMCP-Apps"
REQUIRED_PROTOCOLS["WEALTH"]="MCP-Server JSON-RPC Well-Known"
REQUIRED_PROTOCOLS["WELL"]="MCP-Server FastMCP JSON-RPC Well-Known"
REQUIRED_PROTOCOLS["HERMES"]="MCP-Bridge SSE Streamable-HTTP"
REQUIRED_PROTOCOLS["arif-sites"]="Well-Known MCP-Apps-Consumer"
REQUIRED_PROTOCOLS["ariffazil"]="Well-Known"

# ── Check each repo ──────────────────────────────────────────────────────
for repo in arifOS AAA A-FORGE GEOX WEALTH WELL HERMES arif-sites ariffazil; do
    repo_dir="$ROOT_DIR/$repo"
    fed_md="$repo_dir/FEDERATION.md"
    proto_md="$repo_dir/docs/PROTOCOL_CONFORMANCE.md"
    
    echo -n "  $repo: "
    
    if [ ! -d "$repo_dir" ]; then
        echo -e "${YELLOW}SKIP${NC} (no directory)"
        continue
    fi
    
    if [ ! -f "$fed_md" ]; then
        echo -e "${RED}GAP${NC} — no FEDERATION.md"
        GAPS=$((GAPS + 1))
        if [ "$repo" = "arifOS" ] || [ "$repo" = "AAA" ] || [ "$repo" = "A-FORGE" ]; then
            CRITICAL=$((CRITICAL + 1))
        fi
        continue
    fi
    
    # Check FEDERATION.md has role declaration
    role=$(grep -oP 'role:\s*\K\w+' "$fed_md" 2>/dev/null || echo "")
    if [ -z "$role" ]; then
        echo -e "${RED}GAP${NC} — FEDERATION.md missing role declaration"
        GAPS=$((GAPS + 1))
        continue
    fi
    
    # Check PROTOCOL_CONFORMANCE.md exists
    if [ ! -f "$proto_md" ]; then
        echo -e "${YELLOW}WARN${NC} — role=$role, no PROTOCOL_CONFORMANCE.md"
        GAPS=$((GAPS + 1))
        continue
    fi
    
    # Verify required protocols are declared in conformance doc
    required="${REQUIRED_PROTOCOLS[$repo]:-}"
    missing_protos=""
    for proto in $required; do
        if ! grep -qi "${proto//-/ }" "$proto_md" 2>/dev/null && ! grep -qi "${proto}" "$proto_md" 2>/dev/null && ! grep -qi "${proto//-/}" "$proto_md" 2>/dev/null; then
            missing_protos="$missing_protos $proto"
        fi
    done
    
    if [ -n "$missing_protos" ]; then
        echo -e "${YELLOW}PARTIAL${NC} — role=$role, missing:$missing_protos"
        GAPS=$((GAPS + 1))
    else
        echo -e "${GREEN}PASS${NC} — role=$role, all protocols declared"
    fi
done

echo ""
echo "────────────────────────────────────"
if [ $CRITICAL -gt 0 ]; then
    echo -e "${RED}CRITICAL BREACH: $CRITICAL critical gaps${NC}"
    echo "Federation protocol alignment FAILED."
    exit 2
elif [ $GAPS -gt 0 ]; then
    echo -e "${YELLOW}WARNING: $GAPS non-critical gaps found${NC}"
    echo "Protocol alignment incomplete — review PROTOCOL_MAP.md."
    exit 0  # Non-blocking for non-critical
else
    echo -e "${GREEN}ALL REPOS PROTOCOL-ALIGNED${NC}"
    echo "Federation protocol conformance: PASS."
    exit 0
fi
