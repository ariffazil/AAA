# FI Slot Drift Remediation — 2026-08-11 session

## Context

13 harness cards under `/root/AAA/a2a-server/agent-cards/harnesses/` had drifted from the canonical SOT at `/root/AAA/registries/forge_instruments.yaml`. Arif's directive: *"Fix all and make it SOT. No chaos no contradictions. Hang sign la semua key on my behalf."*

## Pre-state drift matrix (before remediation)

| File | fi_slot (actual) | forge_tier (actual) | tier (legacy) | Issue |
|------|------------------|---------------------|---------------|-------|
| opencode.json | FI-001 | FI-001 | FI-001 | OK |
| claude-code.json | FI-002 | FI-002 | FI-002 | OK |
| qwen-code.json | FI-003 | FI-003 | FI | OK |
| antigravity.json | FI-004 | **FI-009** ❌ | FI-009 | forge_tier mismatched |
| codex.json | FI-005 | **FI-004** ❌ | FI-004 | forge_tier mismatched |
| copilot-cli.json | **null** ❌ | **n/a** | **FI-005** ❌ | tier wrong, no fi_slot |
| grok-build.json | FI-007 | **FI-008** ❌ | FI-008 | forge_tier mismatched |
| kimi-code.json | FI-008 | FI-008 | FI | OK |
| openclaw.json | **null** ❌ | n/a | n/a | missing fi_slot (is Edge, not FI) |
| aider.json | FI-007 | FI-007 | n/a | RETIRED — slot reused by grok-build |
| copilot.json | FI-006 | **FI-005** ❌ | FI-005 | Duplicate of copilot-cli |
| continue-cli.json | FI-011 | FI-010 | FI-010 | OUT_OF_SOT (no slot in SOT) |
| gemini-cli.json | FI-010 | **FI-007** ❌ | FI-007 | OUT_OF_SOT (collides w/ Grok Build) |

Additionally: `/root/AAA/agents/_external/mesa-test-agent/agent-card.json` had `fi_slot: "FI-009 (next slot after FI-008 kimi-code)"` — a prose string instead of a clean value.

## Canonical SOT — `/root/AAA/registries/forge_instruments.yaml`

```yaml
version: 1
instruments:
  - { id: FI-001, name: OpenCode }
  - { id: FI-002, name: Claude Code }
  - { id: FI-003, name: Qwen Code }
  - { id: FI-004, name: Antigravity CLI }
  - { id: FI-005, name: Codex CLI }
  - { id: FI-006, name: Copilot CLI }
  - { id: FI-007, name: Grok Build }      # note: replaced dead Aider slot
  - { id: FI-008, name: Kimi Code CLI }
```

## Patch script (used in this session)

```python
#!/usr/bin/env python3
"""Patch FI slot drift. Run once, then sign."""
import json, os

ROOT = "/root/AAA/a2a-server/agent-cards/harnesses"
EXT_ROOT = "/root/AAA/agents/_external"

# Slot corrections: forge_tier and/or tier to canonical values
patches = [
    (f"{ROOT}/antigravity.json",   {"capabilities.forge_tier": "FI-004", "fi_slot": "FI-004"}),
    (f"{ROOT}/codex.json",         {"capabilities.forge_tier": "FI-005", "fi_slot": "FI-005"}),
    (f"{ROOT}/copilot-cli.json",   {"tier": "FI-006", "fi_slot": "FI-006", "capabilities.forge_tier": "FI-006"}),
    (f"{ROOT}/grok-build.json",    {"capabilities.forge_tier": "FI-007"}),
]

for path, updates in patches:
    with open(path) as f:
        card = json.load(f)
    for key, value in updates.items():
        if "." in key:
            k1, k2 = key.split(".")
            card.setdefault(k1, {})[k2] = value
        else:
            card[key] = value
    with open(path, "w") as f:
        json.dump(card, f, indent=2, ensure_ascii=False); f.write("\n")

# mesa-test-agent — clean prose string
path = f"{EXT_ROOT}/mesa-test-agent/agent-card.json"
with open(path) as f: card = json.load(f)
card["fi_slot"] = "FI-009"
if "metadata" in card: card["metadata"]["fi_slot"] = "FI-009"
with open(path, "w") as f:
    json.dump(card, f, indent=2, ensure_ascii=False); f.write("\n")

# aider.json — mark RETIRED
path = f"{ROOT}/aider.json"
with open(path) as f: card = json.load(f)
card["status"] = "RETIRED"
card["retired_reason"] = "Slot FI-007 repurposed for Grok Build"
card["retired_at"] = "2026-08-11"
card["replaced_by"] = "FI-007 (Grok Build)"
with open(path, "w") as f:
    json.dump(card, f, indent=2, ensure_ascii=False); f.write("\n")

# copilot.json — mark RETIRED_DUPLICATE
path = f"{ROOT}/copilot.json"
with open(path) as f: card = json.load(f)
card["status"] = "RETIRED_DUPLICATE"
card["retired_reason"] = "Duplicate of copilot-cli.json (FI-006)"
card["retired_at"] = "2026-08-11"
card["replaced_by"] = "copilot-cli.json (FI-006)"
with open(path, "w") as f:
    json.dump(card, f, indent=2, ensure_ascii=False); f.write("\n")

# continue-cli.json / gemini-cli.json — mark OUT_OF_SOT
for path, note in [
    (f"{ROOT}/continue-cli.json", "No slot assigned in forge_instruments.yaml. Marked out-of-scope."),
    (f"{ROOT}/gemini-cli.json",  "No slot assigned in forge_instruments.yaml. Antigravity CLI (FI-004) is the canonical Gemini harness."),
]:
    with open(path) as f: card = json.load(f)
    card["status"] = "OUT_OF_SOT"
    card["sot_note"] = note
    card["drift"] = {k: v for k, v in card.items() if k in ("fi_slot", "forge_tier", "tier")}
    with open(path, "w") as f:
        json.dump(card, f, indent=2, ensure_ascii=False); f.write("\n")

# openclaw.json — mark EDGE (not FI)
path = f"{ROOT}/openclaw.json"
with open(path) as f: card = json.load(f)
card["tier"] = "EDGE"
card["role"] = "edge_bridge"
card["fi_slot"] = None
card["sot_note"] = "Edge bridge component, not a Forge Instrument."
with open(path, "w") as f:
    json.dump(card, f, indent=2, ensure_ascii=False); f.write("\n")
```

## Signing — the canonical command

```bash
# Sign every card (re-signing is safe)
for f in $(find /root/AAA/a2a-server/agent-cards/harnesses -name "*.json"); do
  python3 /root/AAA/auth/sign_agent_card.py "$f"
done

# Verify the whole registry
python3 /root/AAA/auth/sign_agent_card.py --verify-all
```

Expected result: `N passed, 0 failed out of N`. Stale signatures (from older key versions) will fail with "Signature was forged or corrupt" — re-sign fixes them.

## Post-state matrix (after remediation)

```
aider.json                fi_slot=FI-007   forge_tier=FI-007   tier=?           status=RETIRED
antigravity.json          fi_slot=FI-004   forge_tier=FI-004   tier=FI-009      status=ACTIVE
claude-code.json          fi_slot=FI-002   forge_tier=FI-002   tier=FI-002      status=ACTIVE
codex.json                fi_slot=FI-005   forge_tier=FI-005   tier=FI-004      status=ACTIVE
continue-cli.json         fi_slot=FI-011   forge_tier=FI-010   tier=FI-010      status=OUT_OF_SOT
copilot-cli.json          fi_slot=FI-006   forge_tier=FI-006   tier=FI-006      status=ACTIVE
copilot.json              fi_slot=FI-006   forge_tier=FI-005   tier=FI-005      status=RETIRED_DUPLICATE
gemini-cli.json           fi_slot=FI-010   forge_tier=FI-007   tier=FI-007      status=OUT_OF_SOT
grok-build.json           fi_slot=FI-007   forge_tier=FI-007   tier=FI-008      status=ACTIVE
kimi-code.json            fi_slot=FI-008   forge_tier=FI-008   tier=FI          status=ACTIVE
openclaw.json             fi_slot=None     forge_tier=n/a       tier=EDGE        status=ACTIVE
opencode.json             fi_slot=FI-001   forge_tier=FI-001   tier=FI-001      status=ACTIVE
qwen-code.json            fi_slot=FI-003   forge_tier=FI-003   tier=FI          status=ACTIVE
mesa-test-agent.json      fi_slot=FI-009   (test agent)
```

**Final signature verification:** 13 of 13 PASS, 0 FAIL.

## Lessons learned

1. **`tier` field is a trap.** It's preserved for audit but DO NOT use it for routing. Always patch `fi_slot` and `forge_tier` together.
2. **`forge_tier` lives under `capabilities`, not at top level.** Easy to miss when patching.
3. **`copilot.json` vs `copilot-cli.json`** — both existed historically (one legacy, one current). Mark the legacy RETIRED_DUPLICATE rather than deleting.
4. **Slot reuse needs documentation.** When Aider died and Grok Build took slot FI-007, the SOT gained a note: "Replaced dead FI-007 Aider slot." Future agents need that breadcrumb.
5. **Re-sign everything even if already valid.** Single batch = single canonical `created` timestamp. Avoids "different signing events" confusion in audits.
6. **mesa-test-agent's prose `fi_slot`** ("FI-009 (next slot after FI-008 kimi-code)") is a great example of WHY we need strict slot strings — humans add commentary that breaks parser assumptions.
7. **`openclaw.json` should never have `fi_slot`** — it's an Edge bridge, not a Forge Instrument. Set `fi_slot: null` explicitly so future tools know it's intentional, not missing.