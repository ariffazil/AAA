# Identity Split v1 — Spec (F13-stage, no build)
**Problem:** `ariffazil/AAA/.gitignore` says exclude `**/identity.json`, but `agents/claude-code/identity.json` IS in GitHub. Policy/repo disagree.

**Solution:** 3-class identity, mechanically obvious which is public.

## Three files

| File | Public? | Contents | Example path |
|---|---|---|---|
| `identity.public.json` | YES (GitHub) | display name, role, avatar URL, public key, agent-card reference | `agents/claude-code/identity.public.json` |
| `identity.private.json` | NO (host only) | private key, credentials, lease, ACT | `~/.claude/identity.private.json` |
| `identity.key` | NO (host only) | raw ed25519 secret | `~/.secrets/identity.key` |

## Schema (`identity.public.json`)

```json
{
  "schema": "arifos.identity.public.v1",
  "agent_id": "claude-code/FI-002",
  "display_name": "Claude Code",
  "role": "governed-executor",
  "public_key": "ed25519:...",
  "agent_card_ref": "agents/claude-code/agent-card.json",
  "federation": "arifOS"
}
```

## Render

- `identity.public.json` ← from AAA repo (canonical)
- `identity.private.json` ← from `/root/.secrets/` (host only, not in git)
- Combined at runtime: `agent.authority = live(arifOS_response)` (NOT from file)

## Why

- F13 stamp on identity ≠ live authority. Per Arif: stamp = provenance, not signal.
- Live authority = `actor_verified` from arifOS response
- Identity.public.json shows WHO, identity.private.json has SECRETS, identity.key has RAW KEY
- Mechanical rule: file extension → commit eligibility

## Migration

- Split existing `agents/claude-code/identity.json` into 2 (public content stays in GitHub, private content moves to host)
- Update `.gitignore` to exclude `identity.private.json` and `identity.key`
- AAA canonical agent-card.json: no key, just role + ceiling + capabilities

## Reversibility

None — this is spec only.
