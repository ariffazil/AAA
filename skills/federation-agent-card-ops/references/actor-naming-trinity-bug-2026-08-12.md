# Actor Naming Trinity Bug — qwen-code/FI-003 → QWEN Sweep (2026-08-12)

**Status:** Forged. Reusable. Class-level lesson.

## The signal

A kernel `arif_init` returns `actor_canonicalized: false`, `actor_verified: false`, `reason_code: NO_IDENTITY_BOUND`, falling through to `session_mode: guest_observe` — despite the actor being Ed25519-exempt and registered. The exemption fires, the registry entry exists, **but canonicalization still fails**. After debugging, the root cause is consistently the same: **three different naming forms for the same actor across three systems**:

```
Registry key:       qwen-code-fi003      ← agent_identities.json
Exemption dict:     qwen-code            ← session_auth.py
Hook-emitted ID:    qwen-code/FI-003     ← settings.json arif_init call
```

The canonicalizer receives `qwen-code/FI-003`, strips and looks for `qwen-code` in the alias tables, finds nothing, returns `None`. The exemption catches the anonymous fallback (no Ed25519 challenge) but the missing canonical match means `actor_canonicalized: false` → fall-through to GUEST.

Compare with **working peers** — every one uses ONE consistent name across all three:

```
claude-code  →  claude-code  →  claude-code     ✓
kimi-code    →  kimi-code    →  kimi-code       ✓
codex        →  codex        →  codex            ✓
qwen-code    →  qwen-code-fi003 → qwen-code/FI-003  ✗
```

## Why this happens

When a new harness (qwen-code, kimi-code, etc.) is bolted into the federation under time pressure, three different sessions each pick "the obvious" name without checking what the other two surfaces call it:

1. **Identity registry writer** picks the role-suffixed name (`qwen-code-fi003`) to avoid collision.
2. **Session auth exemption dict writer** picks the bare name (`qwen-code`) because that's what the Ed25519 exemption key looks like.
3. **Hook / settings.json writer** picks the compound form (`qwen-code/FI-003`) because that's what their arif_init expects.

None of them are wrong alone. All three are wrong together.

## The fix — align to one canonical name

Pick the bare harness name (`qwen-code`) — matches peers, matches the exemption dict, lowest entropy. Three patches:

### Patch 1 — Registry key rename

```bash
# /opt/arifos/identity/agent_identities.json AND /root/A-FORGE/data/agent_identities.json
# "qwen-code-fi003": {...}  →  "qwen-code": {...}
```

Both files must stay in parity (same key count). Drift between them is a separate chaos class.

### Patch 2 — CANONICAL_ACTORS entry

```python
# /root/arifOS/{contracts,arifosmcp/contracts}/identity.py AND /opt/arifos/app/contracts/identity.py
"QWEN": {
    "sovereign_id": "ARIF_FAZIL",
    "default_tier": "AGENT",
    "aliases": ["qwen", "qwen-code", "FI-003", "fi-003"],
},
```

**Symmetry rule:** add QWEN, KIMI, CODEX in uppercase form together. Python dict duplicate keys are silent — the first wins. Found: `codex` (lowercase, line 312) + `CODEX` (uppercase, line 372) both existed; all variants resolved (harmless but chaotic). Removed lowercase, kept uppercase for symmetry.

### Patch 3 — settings.json hooks

```bash
# /root/.qwen/settings.json (or equivalent harness config)
# In SessionStart / SessionEnd / arif_init body:
#   "X-ArifOS-Actor": "qwen-code/FI-003"  →  "X-ArifOS-Actor": "qwen-code"
#   "actor_id": "qwen-code/FI-003"        →  "actor_id": "qwen-code"
#   "forge_instrument": "FI-003"          →  leave alone (FI-003 is the SLOT, not the IDENTITY)
```

`forge_instrument` stays — that's the FI slot, which IS named `FI-003`. Don't conflate identity and slot.

## Detection — the 4-step diagnostic recipe

When ANY session comes back as GUEST despite exemption being in place:

```bash
# 1. Direct kernel probe — see actual reason_code
curl -sS http://127.0.0.1:8088/mcp -X POST \
  -H "Content-Type: application/json" -H "A2A-Version: 1.0" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_init","arguments":{"actor_id":"<suspect>","mode":"init","forge_instrument":"<fi-slot>","f13_directive":"yolo"}}}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['result']['structuredContent']; r=d.get('result',{}); print(r.get('reason_code'), '/', r.get('actor_canonicalized'))"

# 2. Python normalizer matrix — list ALL variant forms
cd /root/arifOS && python3 -c "
from arifosmcp.contracts.identity import normalize_actor_identity
for f in ['qwen-code','qwen-code/FI-003','qwen-code-fi003','QWEN']:
    r=normalize_actor_identity(f); n=r.get('normalized','None') if isinstance(r,dict) else 'None'
    print(f'  {f:20s} → {n}')
"

# 3. Settings.json hook audit — what IS the hook actually sending?
python3 -c "
import json,re
d=json.load(open('/root/.qwen/settings.json'))
all_actors = sorted(set(re.findall(r'qwen-code[/\-_A-Z0-9]*', json.dumps(d))))
print('settings.json actors:', all_actors)
"

# 4. Identity registry parity check
diff <(jq 'keys' /opt/arifos/identity/agent_identities.json) \
     <(jq 'keys' /root/A-FORGE/data/agent_identities.json)
```

The fastest signal is step 2: **if ANY variant form returns None, the canonical aliases don't cover it.** That's the trinity bug.

## Lock-in — commit before kernel reload

The fix is useless until committed. A VPS reboot reverts to clean git. Seal all three repos together:

```bash
# arifOS (Kernel Identity)
cd /root/arifOS
git add contracts/identity.py arifosmcp/contracts/identity.py arifosmcp/runtime/session_auth.py
git commit -m "chore(identity): eradicate qwen-code/FI-003 ghost, enforce canonical QWEN/KIMI/CODEX identity bindings"

# A-FORGE (Registry)
cd /root/A-FORGE
git add data/agent_identities.json litellm-config.yaml
git commit -m "chore(registry): sync agent identities to canonical V3 and update LiteLLM routing"

# AAA (Federation State)
cd /root/AAA
git add federation/STATE.yaml call_map.yaml organs.yaml registries/forge_instruments.yaml TODO.md
git commit -m "docs(federation): update state, mark FI-003 sweep complete, lock canonical actor mapping"
```

## After-action verification

```bash
# ALL forms resolve to ONE canonical
cd /root/arifOS && python3 -c "
from arifosmcp.contracts.identity import normalize_actor_identity, CANONICAL_ACTORS
print(f'Keys ({len(CANONICAL_ACTORS)}): {list(CANONICAL_ACTORS.keys())}')
for a in ['qwen-code','qwen-code/FI-003','qwen-code-fi003','QWEN']:
    r=normalize_actor_identity(a); n=r.get('normalized','FAIL') if isinstance(r,dict) else 'FAIL'
    print(f'  {a:20s} → {n}')
"

# 8 organs healthy, 3 repos clean
for p in 8088 7071 7072 3001 8081 18082 18083 7073; do
  curl -sf --max-time 2 http://127.0.0.1:$p/health >/dev/null && echo "✅ :$p" || echo "❌ :$p"
done
```

## Cross-references

- `federation-identity-reconciliation` — diagnostic ladder for identity drift
- `references/fi-slot-drift-remediation.md` — FI slot hygiene cousin
- `references/i-arif-identity-refactor-2026-08-12.md` — IDENTITY class organ promotion
