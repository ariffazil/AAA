# KIMINA Rollback Procedures

> **Every change has a tested rollback. No rollback = no change.**

## Config Rollback

```bash
# Backup location: /root/.kimi-code/backups/kimina-aaa-<timestamp>/
cp /root/.kimi-code/backups/kimina-aaa-<latest>/config.toml /root/.kimi-code/config.toml
```

## Agent Rollback

```bash
# Remove aaa-* agents (af-* agents untouched)
rm /root/.kimi-code/agents/aaa-*.md
```

## Hook Rollback

```bash
# Remove agentic state hooks from config.toml
# Lines after "# === AGENTIC STATE HOOKS ==="
# Then remove hook scripts
rm /root/.kimi-code/hooks/session_end_state.py
rm /root/.kimi-code/hooks/user_prompt_submit_digest.py
rm /root/.kimi-code/hooks/post_tool_use_track.py
rm /root/.kimi-code/hooks/experience_boot_context.py
```

## Agentic State Rollback

```bash
# Restore from backup
cp /root/.kimi-code/agent_state/backups/kimi-<timestamp>.json /root/.kimi-code/agent_state/kimi.json
# Or nuke and cold-start
rm /root/.kimi-code/agent_state/kimi.json
```

## Restored Skills Rollback

```bash
# Re-delete the restored skills (they were deleted in c3ac34677)
rm /root/AAA/skills/rsi-federation-mesh/SKILL.md
rm /root/AAA/skills/reality-loop-operator/SKILL.md
rm /root/AAA/skills/agi-dream-engine/SKILL.md
rm /root/AAA/skills/kimi-agentic-state/SKILL.md
```

## Full Nuclear Rollback

```bash
# Restore config from pre-upgrade backup
cp /root/.kimi-code/backups/kimina-aaa-<timestamp>/* /root/.kimi-code/
# Remove all new agents
rm /root/.kimi-code/agents/aaa-*.md
# Remove all new hooks
rm /root/.kimi-code/hooks/*.py
# Remove agentic state
rm -rf /root/.kimi-code/agent_state/
# Remove docs
rm /root/AAA/docs/KIMINA-*.md
```

## Ollama Provider Rollback (from 2026-09-16 session)

```bash
# Re-enable KVM8's Ollama
systemctl enable --now ollama
# Restore env files from backup
cp /root/.secrets/vault.flat.env.bak-<stamp> /root/.secrets/vault.flat.env
systemctl daemon-reload && systemctl restart arifos a-forge aaa-a2a
```

DITEMPA BUKAN DIBERI ⚒️
