#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AAA Art Binding Diff Check
# ═══════════════════════════════════════════════════════════════
# Verifies all bound agents reference the canonical binding.
# Exit 0 = clean (all agents bound to canonical)
# Exit 1 = drift detected (reconcile before forging)
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

CANONICAL="/root/AAA/art_binding.canonical.yaml"
AGENTS=(hermes-asi openclaw claude-code opencode)

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   AAA ART BINDING — DIFF CHECK                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Canonical: $CANONICAL"
echo "  Agents:    ${AGENTS[*]}"
echo ""

# ── Check 1: Canonical exists and parses ──
if [ ! -f "$CANONICAL" ]; then
  echo "❌ CRITICAL: Canonical file missing: $CANONICAL"
  exit 2
fi

if ! python3 -c "import yaml; yaml.safe_load(open('$CANONICAL'))" 2>/dev/null; then
  echo "❌ CRITICAL: Canonical YAML fails to parse"
  exit 2
fi
echo "  ✓ Canonical YAML parses"

# ── Check 2: Canonical has all 4 agent entries ──
for agent in "${AGENTS[@]}"; do
  if grep -q "  $agent:" "$CANONICAL"; then
    echo "  ✓ $agent — in canonical registry"
  else
    echo "  ❌ $agent — MISSING from canonical registry"
    DRIFT=1
  fi
done

echo ""

# ── Check 3: Each agent's local stub references canonical ──
DRIFT=0
for agent in "${AGENTS[@]}"; do
  LOCAL="/root/AAA/agents/$agent/art_binding.yaml"
  CARD="/root/AAA/agents/$agent/agent-card.json"

  # Check local stub exists
  if [ ! -f "$LOCAL" ]; then
    echo "  ❌ $agent — local art_binding.yaml MISSING"
    DRIFT=1
    continue
  fi

  # Check local stub parses as YAML
  if ! python3 -c "import yaml; yaml.safe_load(open('$LOCAL'))" 2>/dev/null; then
    echo "  ❌ $agent — local YAML fails to parse"
    DRIFT=1
    continue
  fi

  # Check local stub references canonical
  if grep -q "canonical: /root/AAA/art_binding.canonical.yaml" "$LOCAL"; then
    :
  else
    echo "  ❌ $agent — local stub missing canonical reference"
    DRIFT=1
    continue
  fi

  # Check agent-card.json parses and has canonical_yaml
  if [ -f "$CARD" ]; then
    if python3 -c "
import json
d = json.load(open('$CARD'))
ab = d.get('art_binding', {})
assert ab.get('canonical_yaml') == '$CANONICAL', f'card canonical_yaml mismatch: {ab.get(\"canonical_yaml\")}'
assert ab.get('enabled') == True, 'art_binding not enabled'
" 2>/dev/null; then
      echo "  ✓ $agent — local stub OK, card OK, canonical ref confirmed"
    else
      echo "  ❌ $agent — agent-card.json canonical_yaml mismatch or parsing error"
      DRIFT=1
    fi
  else
    echo "  ⚠ $agent — no agent-card.json (may be intentional)"
  fi
done

echo ""

# ── Check 4: Binding invariant present in canonical ──
if grep -q 'MD declares law' "$CANONICAL"; then
  echo "  ✓ Binding invariant present in canonical"
else
  echo "  ❌ Binding invariant MISSING from canonical"
  DRIFT=1
fi

# ── Check 5: Shared substrate paths correct ──
python3 -c "
import yaml
d = yaml.safe_load(open('$CANONICAL'))
subs = d['canonical']['substrates']
assert subs['md']['path'] == '/root/.agents/skills/CONSTITUTIONAL_REFLEX/SKILL.md'
assert subs['schema']['path'] == '/root/arifOS/arifosmcp/schemas/art.py'
assert subs['code']['path'] == '/root/arifOS/arifosmcp/runtime/art.py'
assert subs['json']['path'] == '/agent/vault999/receipts/outcomes.jsonl'
" 2>/dev/null && echo "  ✓ Shared substrate paths verified"

echo ""
echo "──────────────────────────────────────────────────────────"
if [ $DRIFT -eq 0 ]; then
  echo "  ╔════════════════════════════════════════════════════╗"
  echo "  ║  ✅ ALL AGENTS BOUND TO CANONICAL — ZERO DRIFT   ║"
  echo "  ╚════════════════════════════════════════════════════╝"
  echo ""
  echo "  1 canonical file → 4 agent stubs → 4 agent cards"
  echo "  DITEMPA BUKAN DIBERI — Forged, Not Given."
  exit 0
else
  echo "  ╔════════════════════════════════════════════════════╗"
  echo "  ║  ❌ DRIFT DETECTED — reconcile before forging    ║"
  echo "  ╚════════════════════════════════════════════════════╝"
  exit 1
fi
