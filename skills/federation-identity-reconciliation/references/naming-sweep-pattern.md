# Identity Naming Sweep — Pattern Reference

Companion to `federation-identity-reconciliation` SKILL.md "Ed25519-Exempt Actor Naming Ceiling" section.

## When to run a naming sweep

- A coding harness (qwen-code, claude-code, codex, kimi-code) consistently returns `GUEST-xxx` sessions
- Logs show multiple actor_id formats for the same logical agent (e.g. `qwen-code` vs `qwen-code/FI-003` vs `qwen-code-fi003`)
- Multiple registries disagree on which keys map to which agents
- Memory files / docs use role labels as if they were identities

## The qwen-code sweep (reference case, 2026-08-12)

### Input state

| File | Had | Should be |
|---|---|---|
| `/root/.qwen/settings.json` (MCP headers) | `qwen-code/FI-003` | `qwen-code` |
| `/root/.qwen/settings.json` (hook commands) | `actor_id="qwen-code/FI-003"` | `actor_id="qwen-code"` |
| `/root/QWEN.md` | "Qwen Code (FI-003)" | "Qwen Code" (with FI-003 as role only) |
| `/opt/arifos/identity/agent_identities.json` | `qwen-code-fi003` key | `qwen-code` key |
| `/root/A-FORGE/data/agent_identities.json` | (missing entry) | `qwen-code` entry |
| `/opt/arifos/app/contracts/identity.py` | missing from CANONICAL_ACTORS | included (already had aliases `["qwen", "qwen-code", "FI-003", "fi-003"]`) |
| `/root/AAA/TODO.md` | "Fix qwen-code (FI-003) Actor Binding" entry | marked DONE |

### Probe-before-patch verification

For each change, the verification step was the **canonical-name-or-not** binary check:

1. Live `kunci-mas.env` / `flat.env` / `config.yaml` — must be empty for retired refs
2. Live skill SKILL.md files — must mark retired refs with explicit annotation
3. Memory files (`.md` in `~/.qwen/memories/`) — historical FI-003 references preserved (not mutated)
4. Backup directories (.bak, archive, quarantine) — never mutated

### Decision rule for FI-XXX references

| Location | FI-XXX reference is… | Action |
|---|---|---|
| `forge_instrument` field | correct (role label) | keep |
| `actor_id` field | wrong (identity confusion) | replace with canonical name |
| `aliases` list in `identity.py` | correct (normalization aliases) | keep |
| MCP header values | wrong (should be canonical) | replace |
| Hook `actor_id` values | wrong | replace |
| Doc/file headings | context-dependent — preserve if historical, refresh if active | selective |
| Memory feedback files | correct as historical context | keep unchanged |

## Verification command — three-tree identity.py match

```bash
md5sum /opt/arifos/app/contracts/identity.py \
       /root/arifOS/contracts/identity.py \
       /root/arifOS/arifosmcp/contracts/identity.py
```

All three hashes must match. If they don't:

1. The deployed runtime is `/opt/arifos/app/contracts/identity.py` — treat it as canonical
2. Copy it over the source trees
3. Redeploy arifOS via systemd

## Two-registry sync — diagnostic + recipe

```bash
python3 << 'PYEOF'
import json
opt = json.load(open('/opt/arifos/identity/agent_identities.json'))
forge = json.load(open('/root/A-FORGE/data/agent_identities.json'))
opt_keys = set(opt.keys())
forge_keys = set(forge.keys())

missing = opt_keys - forge_keys
extra = forge_keys - opt_keys

print(f"/opt/arifos entries: {len(opt)}")
print(f"A-FORGE entries: {len(forge)}")
if missing:
    print(f"MISSING in A-FORGE: {sorted(missing)}")
if extra:
    print(f"EXTRA in A-FORGE: {sorted(extra)}")
if not missing and not extra:
    print("✅ Synced")

# Sync A-FORGE <- /opt/arifos (A-FORGE is downstream)
for k in sorted(missing):
    forge[k] = opt[k]
with open('/root/A-FORGE/data/agent_identities.json', 'w') as f:
    json.dump(forge, f, indent=2)
print(f"Synced {len(missing)} entries")
PYEOF
```

## Key insight: the GUEST ceiling is structural, not fixable

After a perfect naming sweep, qwen-code, claude-code, and codex STILL return:
- `actor_verified: false`
- `actor_canonicalized: false`
- `session_id: GUEST-xxx`
- `authority_band: OBSERVE_ONLY`

This is not a bug to fix — it's the F1 Amanah ceiling for Ed25519-exempt actors. The naming sweep doesn't get them to SEAL-xxx; it only:
- Makes audit trails unambiguous
- Eliminates the appearance of multiple "agents" (qwen-code, qwen-code/FI-003, qwen-code-fi003) when there's actually one
- Lets the registered canonical name in the system, not the slash-form baggage

The path from GUEST-xxx to SEAL-xxx for a coding harness requires:
1. Ed25519 key generation (keypair per actor)
2. Cryptographic binding to a session via SCT (signed capability token)
3. Federation-wide consensus approval

This is intentional design. Coding harnesses without crypto proof are observer-class by F1. They cannot mutate, but they can be relied upon to talk truth about what they observe.

## Related

- `arifos-federation-ops` — federation runtime operations
- `arifos-prompt-doctrine` — editing prompt-stack files
- `kernel-security-claim-audit` — verifying security claims about the kernel

*DITEMPA BUKAN DIBIRI — one canonical name per agent, four backups preserved, three registries in sync.*