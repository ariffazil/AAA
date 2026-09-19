# Audit findings — federation-shadow-ack-20260919

**Auditor:** codex (FI-005)
**Date:** 2026-09-19
**Verdict:** 2 defects found, both T1 reversible.

## DEFECT-1 — qwen-code shadow entry is a 4-way split

**File:** `/root/AAA/agents/_external/qwen-code/agent-card.json`
**Field:** `shadowAcknowledged[0..3]` should be one entry, got split into four by line break inside the gloss.
**Repro:**
```python
import json
d = json.load(open('/root/AAA/agents/_external/qwen-code/agent-card.json'))
print(len(d['shadowAcknowledged']))  # 6 — should be 3
for s in d['shadowAcknowledged'][:4]:
    print(repr(s))
# 'sparse_history: shadow-matrix shows state=STUCK'
# 'BALANCED, fq=0.25'
# '1.0, execute_count=8'
# '1 — too little signal to diagnose a blind spot; truth-class for any qwen-code claim stays DERIVED not MEASURED until traffic grows'
```

**Fix:** collapse [0..3] into a single string entry:
```
"sparse_history: shadow-matrix shows qwen-code at STUCK/BALANCED fq=0.25, execute_count=8, verify_count=1 — too little signal to diagnose a blind spot; truth-class for any qwen-code claim stays DERIVED not MEASURED until traffic grows"
```

**Risk:** T1 (single field edit). Reversible via `.bak-2026-09-19-shadow-ack`.

## DEFECT-2 — `covers_shadow_ids` is empty on all 12 script-populated cards

**Files:** `/root/AAA/agents/_external/{agy,aider,claude-code,continue-cli,copilot,copilot-cli,grok,grok-build,kimi-code,mesa-test-agent,opencode,qwen-code}/agent-card.json`
**Field:** `shadow_population_meta.covers_shadow_ids`
**Expected:** array of divergence registry ids this shadow entry addresses (e.g., `["DIV-CODEX-SHADOW-SPARSE"]` on the codex card).
**Found:** `[]` on all 12 script-populated cards. Only codex's hand-edited card has the field populated.

**Repro:**
```python
import json, os
for d in sorted(os.listdir('/root/AAA/agents/_external')):
    p = f'/root/AAA/agents/_external/{d}/agent-card.json'
    if not os.path.exists(p): continue
    c = json.load(open(p))
    covers = c.get('shadow_population_meta', {}).get('covers_shadow_ids', 'missing')
    print(f'{d}: {covers}')
# agy: []
# aider: []
# claude-code: []
# ...
# codex: ['DIV-CODEX-SHADOW-SPARSE', 'DIV-CODEX-DUAL-HOME']
```

**Fix:** patch `/root/AAA/scripts/populate-shadow-acknowledged.sh` to set `covers_shadow_ids` per card. Re-run with new `.bak-2026-09-19-shadow-ack-v1` backups (rotate old `.bak` files first).

**Suggested mapping (DERIVED — codex's best inference, not MEASURED):**

| Card | covers_shadow_ids (suggested) |
|---|---|
| agy | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` (sparse) — agy is antigravity; if it has its own divergence, use that id |
| aider | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| claude-code | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| continue-cli | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| copilot | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| copilot-cli | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| grok | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| grok-build | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| kimi-code | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| mesa-test-agent | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| opencode | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |
| qwen-code | `["DIV-FEDERATION-SHADOW-ACK-CLOSED"]` |

(Real shadow ids can be found in `/root/AAA/docs/deprecation-registry.json` open_divergences list, but none of the 12 affected cards had pre-existing divergence entries beyond DIV-FEDERATION-SHADOW-ACK-CLOSED itself.)

**Risk:** T1 (script edit + re-run). Each re-run overwrites an existing `.bak-2026-09-19-shadow-ack` — rotate to `v1` first.

## Companion status

`DIV-FEDERATION-SHADOW-ACK-CLOSED` should be re-opened to `PARTIALLY_CLOSED` until both defects are patched. `closure:` field should reference this FINDINGS file.
