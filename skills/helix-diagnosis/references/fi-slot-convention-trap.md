# FI Card Slot Convention Trap

**Date:** 2026-08-11  
**Session:** Multiple agents discovered this independently (333-AGI, Kimi Code/FI-008)  
**Severity:** MEDIUM — prevents correct FI registration in AAA registry  

## The Trap

FI cards use **TWO fields** that look almost identical:

```json
{
  "tier": "FI",                    // ← should be literal string "FI"
  "fi_slot": "FI-003"              // ← actual FI identifier
}
```

### Wrong Pattern (What Went Wrong)

```json
{
  "tier": "FI-011",                // ❌ WRONG — copied fi_slot into tier!
  "fi_slot": "FI-003"              // Correct but ignored
}
```

When `tier` contains the full slot (`FI-XXX`), the system:
- Cannot distinguish "which FI am I?" from "what category of tool am I?"
- Treats tier as an identity marker instead of a capability class
- Creates duplicate/conflicting registrations in AAA's registry

## Evidence from Session

### What My Analysis Initially Got Wrong

My first pass analysis assumed `tier` and `fi_slot` were interchangeable or redundant. This led to:
- Incorrect architecture mapping ("Qwen Code is FI-011" when it's actually FI-003)
- Confusing which tools occupy which slots
- Suggesting fixes that would have made things worse

### What Kimi Code Discovered Independently

Kimi Code ran a live audit of `/root/AAA/_external/*/agent-card.json` files and found:
- All other valid FI cards use `tier: "FI"` with `fi_slot: "FI-XXX"` pattern
- Qwen Code and Kimi Code harnesses had swapped these values
- Binary paths also drifted (`/usr/bin/qwen` vs `/root/.local/bin/qwen`)

This wasn't my error alone — it was a systemic pattern where multiple agents misread the convention.

## Why It Matters

The `tier` field tells arifOS what **class of power** this FI represents:
- `tier: "FI"` = Federated Instrument (standard tool, replaceable, bounded autonomy)
- Values like `"FI-011"` break this categorization

The `fi_slot` field tells AAA **where this FI lives** in the registry:
- `fi_slot: "FI-003"` = mapped entry at index 003 in `/root/AAA/registries/forge_instruments.yaml`
- This is the source-of-truth mapping used by A2A routing

If you swap them, routing breaks: the daemon looks up slot 011, finds nothing, assumes tool doesn't exist.

## Fix Pattern

### Before (Broken)
```json
{
  "tier": "FI-011",
  "fi_slot": "FI-003",
  "capabilities": { ... }
}
```

### After (Correct)
```json
{
  "tier": "FI",
  "fi_slot": "FI-011",            // ← match tier category with slot ID
  "capabilities": { ... }
}
```

Note: The slot ID must match the tier's position in the registry. If Qwen Code is FI-011, then fi_slot must be `"FI-011"`, not `"FI-003"`.

## Verification Script

Run this after editing any FI card:

```bash
#!/bin/bash
# Check all external agent-cards for consistency

for card in /root/AAA/_external/*/*/agent-card.json; do
  if grep -q '"fi_slot"' "$card"; then
    slot=$(python3 -c "import json,sys; print(json.load(open('$card'))['fi_slot'])")
    tier=$(python3 -c "import json,sys; print(json.load(open('$card'))['tier'])")
    
    if [ "$tier" != "FI" ]; then
      echo "⚠️ $card has tier='$tier' instead of 'FI'"
    elif [[ "$slot" == *"FI-"* ]] && [ "${slot#"FI-"}" -ge 0 ] 2>/dev/null; then
      echo "✅ $card OK: tier=FI, fi_slot=$slot"
    else
      echo "⚠️ $card slot format unclear: $slot"
    fi
  fi
done
```

Or alternatively, use jq for JSON parsing:

```bash
jq -r '.fi_slot, .tier' /root/AAA/_external/*/agent-card.json | paste - - | awk '{print $1, $2}'
```

Expected output (all tiers should be "FI"):
```
FI-001  FI
FI-002  FI
...
```

## Related Fixes

- Commit 5b1192f9 (`fix(aaa): reconcile FI card tier/slot drift + refresh FI-003 SOT to live reality`)
- FQ P0 case study (`references/fq-drift-case-study-2026-08-11.md`) — same root cause: direct writes bypassing canonical channels
- Seven Verbs Doctrine (`EUREKA-T-02-seven-verbs-helix.md`) — clarifies that Register (AAA) owns identity mapping while Measure (FRAME) owns drift observation

## Common Pitfalls

1. **Assuming tier=f-slot means they're interchangeable** — They're NOT. One describes class (tier), one describes location (slot).

2. **Copying fi_slot value into tier field** — This happens when editing nested JSON structures blindly. Always verify both fields after bulk-edit sessions.

3. **Registry mismatch** — Editing `fi_slot` without updating `/root/AAA/registries/forge_instruments.yaml` creates stale mappings. Run a registry sweep after changes.

4. **Binary path drift** — Another common FI card bug. Binary paths change over time (`/usr/bin/tool` → `/root/.local/bin/tool`). Verify paths quarterly via `which tool`.

## See Also

- [`FI_INTEGRATION_ARCHITECTURE.md`](/root/AAA/canon/FI_INTEGRATION_ARCHITECTURE.md) — single-page canon for FI lifecycle
- [`organs.yaml`](/root/AAA/federation/organs.yaml) — line range for AAA registrar role definition
