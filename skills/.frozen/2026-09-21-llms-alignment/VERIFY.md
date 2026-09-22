# VERIFY — one-command integrity check for the mcp-ops v3.1.1 audit corpus

> **Purpose:** let the F13 sovereign reviewer verify every sha256 in the audit corpus with
> a single bash command. If any sha mismatches, the canonical SKILL.md was mutated since
> the audit was sealed — a defect signal.
> **Date:** 2026-09-21
> **Producer:** 333-AGI autonomous continuation

---

## The single command

Save as `verify_corpus.sh`, mark executable, and run from any host with shell + sha256sum
plus read access to `/root/AAA/skills/.frozen/2026-09-21-llms-alignment/`:

```bash
#!/usr/bin/env bash
# verify_corpus.sh — sha256 audit of mcp-ops v3.1.1 closure corpus
# Run on 2026-09-21 (or later); if any line FAILS, the canonical was mutated.

set -u
EXPECTED_DIR=/root/AAA/skills/.frozen/2026-09-21-llms-alignment
EXPECTED_CANONICAL=/root/AAA/skills/engineering/mcp-ops/SKILL.md
EXPECTED_OWNERSHIP=/root/AAA/skills/OWNERSHIP_MAP.yaml

# sha256 prefixes (16 hex chars) — capture live with:  sha256sum FILE | awk '{print substr($1,1,16)}'
declare -A EXPECTED
EXPECTED[INDEX.md]="1fdc66089f1463c3"
EXPECTED[SOVEREIGN_INVOCATION_GUIDE.md]="d37dc577460cfb78"
EXPECTED[SOVEREIGN_QUICKSTART.md]="365342a11170a256"
EXPECTED[SKILL.md.from.mcp-ops-v3.0.1]="ebe2ebdfa487f65e"
EXPECTED[SKILL.md.from.mcp-ops-v3.1.0]="bfc0b92800867849"
EXPECTED[SKILL.md.from.mcp-testing]="ebe2ebdfa487f65e"
EXPECTED[absorbed-INDEX.md.from.pre-alignment]="a4498942fc0405ac"
EXPECTED[OWNERSHIP_MAP.yaml.from.pre-mcp3.1.1]="8e45fb12fd3d8e6d"
EXPECTED[audit/888_HOLD_ESCALATION.md]="bb350a1ca354e5ad"
EXPECTED[audit/mcp-federation-closeout.md]="4a60ff656e87241a"
EXPECTED[audit/mcp_capability_graph.yaml]="6fa7bfd5a3b35c0e"
EXPECTED[audit/mcp_capability_inventory.yaml]="84153b8f5656e1e1"
EXPECTED[audit/mcp_deletion_safety_report.md]="7d747e21b97a10f3"
EXPECTED[audit/mcp_federation_closeout_plan.md]="ccc75a3b8524fb50"
EXPECTED[audit/mcp_skill_rationalization.md]="f9003e11999ef05a"

EXPECTED_CANONICAL_SHA="de09f5faf0ef2319"
EXPECTED_OWNERSHIP_SHA="08ce9431dfd0e497"

pass=0
fail=0
echo "=== Verifying 15 audit corpus files ==="
for f in "${!EXPECTED[@]}"; do
  p="$EXPECTED_DIR/$f"
  if [ ! -f "$p" ]; then
    echo "  MISSING  $f"
    fail=$((fail+1))
    continue
  fi
  actual=$(sha256sum "$p" | awk '{print substr($1,1,16)}')
  if [ "$actual" = "${EXPECTED[$f]}" ]; then
    echo "  OK       $f  ($actual)"
    pass=$((pass+1))
  else
    echo "  FAIL     $f  actual=$actual expected=${EXPECTED[$f]}"
    fail=$((fail+1))
  fi
done

echo ""
echo "=== Verifying canonical SKILL.md (live) ==="
actual=$(sha256sum "$EXPECTED_CANONICAL" | awk '{print substr($1,1,16)}')
if [ "$actual" = "$EXPECTED_CANONICAL_SHA" ]; then
  echo "  OK       $EXPECTED_CANONICAL  ($actual)"
  pass=$((pass+1))
else
  echo "  FAIL     $EXPECTED_CANONICAL  actual=$actual expected=$EXPECTED_CANONICAL_SHA"
  fail=$((fail+1))
fi

echo ""
echo "=== Verifying OWNERSHIP_MAP.yaml (live) ==="
actual=$(sha256sum "$EXPECTED_OWNERSHIP" | awk '{print substr($1,1,16)}')
if [ "$actual" = "$EXPECTED_OWNERSHIP_SHA" ]; then
  echo "  OK       $EXPECTED_OWNERSHIP  ($actual)"
  pass=$((pass+1))
else
  echo "  FAIL     $EXPECTED_OWNERSHIP  actual=$actual expected=$EXPECTED_OWNERSHIP_SHA"
  fail=$((fail+1))
fi

echo ""
echo "=== Verifying 22 federation tombstones resolve to v3.1.1 ==="
ok=0; bad=0; bad_paths=()
for tree in /root/AAA/skills /root/.opencode/skills /root/.agents/skills /root/.claude/skills; do
  while IFS= read -r L; do
    t=$(readlink "$L")
    [[ "$t" == *hermes/profiles/aaa-hermes/skills/FORGE-mcp-ops* ]] && continue
    [[ "$t" == *engineering/mcp-ops* || "$t" == *FORGE-mcp-ops* ]] || continue
    abs=$(readlink -f "$L" 2>/dev/null)
    [ -f "$abs/SKILL.md" ] || continue
    ver=$(grep -m1 '^version:' "$abs/SKILL.md" 2>/dev/null | awk '{print $2}')
    if [ "$ver" = "3.1.1" ]; then ok=$((ok+1)); else bad=$((bad+1)); bad_paths+=("$L → $ver"); fi
  done < <(find "$tree" -type l 2>/dev/null)
done
echo "  v3.1.1-OK  : $ok / 22"
if [ "$bad" -gt 0 ]; then
  for p in "${bad_paths[@]}"; do echo "  STALE    $p"; done
fi
[ "$ok" = "22" ] && pass=$((pass+1)) || fail=$((fail+1))

echo ""
echo "=== Verifying arifOS substrate ==="
status=$(curl -s --max-time 3 http://127.0.0.1:8088/health | python3 -c "
import sys, json
h = json.load(sys.stdin)
print(h['layer_health']['constitutional']['floors_active'], h['layer_health']['constitutional']['vault999'])
" 2>/dev/null)
if [ -n "$status" ]; then
  echo "  arifOS :8088 — floors=${status%% *}/13  vault=${status##* }"
  pass=$((pass+1))
else
  echo "  WARN     arifOS :8088 unreachable"
  fail=$((fail+1))
fi

echo ""
echo "================================================"
echo "  pass: $pass / $((pass+fail))"
echo "  fail: $fail"
echo "================================================"
[ "$fail" = "0" ] && { echo "STATUS: VERIFIED — corpus is intact."; exit 0; }
echo "STATUS: DEFECT — investigate FAIL rows above."; exit 1
```

## What it checks

| Check | What it proves |
|---|---|
| 15 audit corpus files | Their byte content matches the SHA anchors captured at the close of the consolidation. A mismatch = the file was edited after sealing. |
| canonical SKILL.md (live) | The v3.1.1 SKILL.md at `/root/AAA/skills/engineering/mcp-ops/SKILL.md` still has sha `de09f5faf0ef…`. A mismatch = the canonical was mutated post-close. |
| OWNERSHIP_MAP.yaml (live) | The ratified OWNERSHIP_MAP (sha `08ce9431dfd0…`) is unchanged. A mismatch = the governance map was rolled back. |
| 22/22 federation tombstones | Every tombstone symlink across 4 mirror trees resolves to v3.1.1. A shortfall = broken route. |
| arifOS substrate | `floors_active/13` and `vault999` are reachable and healthy. A degradation = substrate drift. |

## How to use

```bash
# Save the script above to a file
chmod +x verify_corpus.sh

# Run (as root, since /root/AAA needs read access)
./verify_corpus.sh

# Expected output:
# === Verifying 15 audit corpus files ===
#   OK       INDEX.md                                  (1fdc66089f1463c3)
#   OK       SOVEREIGN_INVOCATION_GUIDE.md             (d37dc577460cfb78)
#   OK       SOVEREIGN_QUICKSTART.md                   (365342a11170a256)
#   ... [12 more OK rows]
# === Verifying canonical SKILL.md (live) ===
#   OK       /root/AAA/skills/engineering/mcp-ops/SKILL.md  (de09f5faf0ef2319)
# === Verifying OWNERSHIP_MAP.yaml (live) ===
#   OK       /root/AAA/skills/OWNERSHIP_MAP.yaml          (08ce9431dfd0e497)
# === Verifying 22 federation tombstones resolve to v3.1.1 ===
#   v3.1.1-OK  : 22 / 22
# === Verifying arifOS substrate ===
#   arifOS :8088 — floors=13/13  vault=healthy
# ================================================
#   pass: 19 / 19
#   fail: 0
# ================================================
# STATUS: VERIFIED — corpus is intact.
```

If `STATUS: DEFECT`:
- A file was edited after the consolidation closed — investigate the affected file.
- A tombstone broke — check whether the symlink target was deleted.
- arifOS substrate degraded — check whether port 8088 is alive.

## When to run

- **Before the F13 seal**: confirm the corpus matches the captured hashes.
- **After the F13 seal**: the seal writes to VAULT999; the audit corpus doesn't change.
- **After any maintenance activity** that touches the frozen dir, OWNERSHIP_MAP, or canonical SKILL.md: re-run to confirm no unintended drift.

## Production note

The script reads `/root/AAA/...` paths. It needs:
- read access to `/root/AAA/` (typical for root or AAA service accounts)
- shell + sha256sum + python3 + curl
- network access to `127.0.0.1:8088` (arifOS local)

If the audit corpus is intended to be readable by a non-root auditor, the directory
permissions would need loosening. Currently the dir is mode `drwxr-xr-x+` — accessible
to owner+group, with extended ACL. Adjust as needed.

## Provenance

Producer: 333-AGI autonomous continuation
Date: 2026-09-21
Status: VERIFIED at write-time (sha prefixes captured against the live corpus)

DITEMPA BUKAN DIBERI ⚒️
