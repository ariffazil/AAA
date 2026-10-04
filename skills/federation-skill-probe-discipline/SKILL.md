---
name: federation-skill-probe-discipline
description: "Discipline for probing whether a skill/plugin/config artifact EXISTS in the arifOS federation. Must enumerate ALL roots before claiming 'absent'. Born from 2026-08-08 BIJAKSANA×BANGANG verification miss where 4 artifacts existed at non-obvious paths."
version: 1.0.0
tags: [meta, probe, verification, F2, F11, paths]
platforms: [linux, macos]
---

# Federation Skill / Config Probe Discipline

When a user asks "does skill X exist?" or "is plugin Y wired?" — **do not answer from one path.** Federation has multiple roots. Single-path probing produces false negatives and breaks F2.

## The 6 skill roots you MUST check

```bash
# 1. Hermes runtime profile (active when running under aaa-hermes profile)
ls /usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/

# 2. Hermes default profile (other profiles)
ls /usr/local/lib/hermes-agent/profiles/*/skills/

# 3. Federation canonical SOT — AAA skill registry (most skills live HERE)
ls /root/AAA/skills/

# 4. AGI workspace skills
ls /root/.agents/skills/ 2>/dev/null

# 5. User home skills (default hermes location)
ls ~/.hermes/skills/ 2>/dev/null

# 6. Symlink-style external dirs (declarable in config.yaml → skills.external_dirs)
```

**Rule:** a skill is **declared absent** only after all 6 roots return empty. Document which roots were probed in your F2 evidence.

## The 3 acpx / Claude Code config roots

acpx + Claude Code do NOT live at the obvious paths. Probe these:

```bash
# 1. OpenClaw plugin config (acpx lives here in OpenClaw, not ~/.acpx/)
python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); print(d.get('plugins',{}).get('entries',{}).get('acpx',{}).get('config',{}))"

# 2. Claude Code settings (5KB+ JSON with permissions, hooks, enabledPlugins, plugins)
cat /root/.claude/settings.json | python3 -m json.tool

# 3. Claude Code skills-directory symlinks (NOT plugins/)
ls -la /root/.claude/skills/  # each is a symlink to a real skill dir
ls /root/.claude/plugins/      # only marketplace-installed plugins live here
```

**Pitfall:** confusing `~/.claude/plugins/` (marketplace) with `~/.claude/skills/` (skills-directory load path). A plugin declared `enabledPlugins` in settings.json loads via skills-directory; the symlink target is the real location.

## The `defaultMode` vs `permissionMode` distinction

Both are F12-relevant but different mechanisms:

| Mode | Mechanism | F12 risk |
|------|-----------|----------|
| `defaultMode: "auto"` | CC silently approves all tool calls | **HIGH** — silent, no audit |
| `defaultMode: "acceptEdits"` | CC auto-approves Edit/Write only; prompts on Bash/MCP | LOW — edits only, Bash audited |
| `permissionMode: "approve-all"` (acpx) | Override Claude Code's permission prompts entirely | **HIGH** — silent |
| `permissionMode: "plan"` (acpx) | Forces plan-first mode, no execution without approval | LOW — gated |

**Both `defaultMode: auto` AND `permissionMode: approve-all` are F12 holes.** They fix differently:
- Claude Code: `defaultMode` → `acceptEdits` (close silent-approve path)
- acpx: `permissionMode` → `plan` (close silent-execute path)

When checking F12 status, probe BOTH paths.

## The verification report must enumerate probed paths

```
## Probe Results (F2 evidence template)

| Artifact | Root 1 | Root 2 | Root 3 | Root 4 | Root 5 | Root 6 | Found at |
|----------|--------|--------|--------|--------|--------|--------|----------|
| skill X  | ✅ path1 | ❌ | ❌ | ❌ | ❌ | ❌ | `/root/AAA/skills/X/` |
| plugin Y | ...     | ...  | ...  | ...  | ...  | ...  | ...           |
```

Never write "X exists at [single path]" without listing what other paths were searched.

## Failure modes from this session (2026-08-08)

**Verifier (me) said:** "hermes-claude-code-spawn skill absent" → probed only `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/autonomous-ai-agents/` and didn't find it.

**Arif's correction:** the skill lives at `/root/AAA/skills/hermes-claude-code-spawn/SKILL.md` (5.1KB) — the federation SOT root, NOT the profile runtime root.

**Lesson:** probe the SOT before the runtime. The SOT (AAA) defines what's authoritative; the runtime (profile) loads what fits its toolset.

## Pitfalls

- **Don't trust `~/.claude/plugins/`** for federation plugins — federation uses `~/.claude/skills/` (skills-directory load) not plugins marketplace.
- **Don't trust `~/.acpx/agents.yaml`** — acpx config in OpenClaw lives in `/root/.openclaw/openclaw.json` under `plugins.entries.acpx.config`.
- **Don't trust `defaultMode: auto` as "stricter than approve-all"** — both are F12 holes; different mechanisms. `auto` is silent, `approve-all` is override.
- **Don't trust single-path "absent" claims** without enumerating all 6 skill roots + 3 CC config roots.
- **Skills symlink vs copy** — federation uses symlinks (`AAA/skills/X → /usr/local/lib/...`) for shadowing. Edit the source, not the symlink target.

## The Axiom

> **Probe ALL roots. Declare absent only after enumeration.**
> F11 Auditability = every absence claim cites the paths searched.
> Path-blind probing is a verifier failure mode, not a user-error.
