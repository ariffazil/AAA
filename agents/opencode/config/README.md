# OpenCode Config Ownership (F13 2026-10-14)

SOT owner: AAA (this directory = pointer + policy).
Machine truth: `/root/.config/opencode/` — git-tracked IN PLACE (baseline fa1fe72).

- `opencode.json` — rendered/deployed config (13 providers, 9 agents, fed+kimi lanes). Edit in place; commit there. AAA references; does not duplicate.
- `plugins/arif-core` — federation hook plugin; delegates to `/root/AAA/hooks/lib/federation_hook_engine.py` (single enforcement point).
- Drift check (weekly housekeeping): `git -C /root/.config/opencode status --porcelain` must be empty or explained.
- Stale July skeleton `config.yaml` (model=deepseek-v4-pro, no consumers) archived to `_archive/config.yaml.stale-20260721`.

Rule: machine delta vs upstream = data layer (config/plugins/rules) → git here, owned by AAA identity.
Upstream binary (npm opencode) → NEVER enters AAA. Not a fork.

## v2 instructions[] finding (2026-10-14, commit 4999b3a)

OpenCode V2 **does not resolve** the config `instructions` array (docs: opencode.ai/v2/docs/plugins → AGENTS.md page). Verified live on v2.0.28: DOCTRINE.md / DOMAIN.md / rules/arifos-governance.md / OPENCODE_SKILL_PROFILE.json were parsed-but-never-loaded — zero session context across all sessions.

Migration:
- Load-bearing rules (FED lanes, model chains, SOT pointers) → folded into global `AGENTS.md` (the v2 mechanism; live-update confirmed same session).
- DOCTRINE.md / DOMAIN.md → remain AAA reference docs. Their agent-specific load is already carried by working `{file:}` agent prompts (333-AGI.md etc.) + AGENTS.md global. ~90% content overlap confirmed.
- `instructions` array removed from opencode.json (4999b3a). If upstream V2 later resolves it, re-add deliberately — do not assume.
