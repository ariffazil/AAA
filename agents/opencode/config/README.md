# OpenCode Config Ownership (F13 2026-10-14)

SOT owner: AAA (this directory = pointer + policy).
Machine truth: `/root/.config/opencode/` — git-tracked IN PLACE (baseline fa1fe72).

- `opencode.json` — rendered/deployed config (13 providers, 9 agents, fed+kimi lanes). Edit in place; commit there. AAA references; does not duplicate.
- `plugins/arif-core` — federation hook plugin; delegates to `/root/AAA/hooks/lib/federation_hook_engine.py` (single enforcement point).
- Drift check (weekly housekeeping): `git -C /root/.config/opencode status --porcelain` must be empty or explained.
- Stale July skeleton `config.yaml` (model=deepseek-v4-pro, no consumers) archived to `_archive/config.yaml.stale-20260721`.

Rule: machine delta vs upstream = data layer (config/plugins/rules) → git here, owned by AAA identity.
Upstream binary (npm opencode) → NEVER enters AAA. Not a fork.
