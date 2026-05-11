---
name: aaa-hermes-workspace-org
description: Organize and wire a Hermes Agent workspace into the AAA repo — identity files, MCP servers, skills, observability, backup cron, and gitignore hygiene. Activate when auditing or setting up Hermes Agent for Arif.
category: devops
version: 1.0.0
author: Arif Fazil
tags: [hermes, AAA, backup, gitignore, workspace-organization]
trigger: Hermes Agent workspace organization or backup setup
---

# AAA Hermes Workspace Organization

## What This Is

Setup and wiring guide for a Hermes Agent installation into the `ariffazil/AAA` repo.
Covers: identity files, MCP servers, skills external_dirs, observability config, backup cron, and AAA agent registry.

---

## Common Pre-conditions

- AAA repo at `/root/AAA`
- Hermes config at `~/.hermes/config.yaml`
- `gh` CLI authenticated as `ariffazil`

---

## Step 1 — Identify the Workspace

```bash
# Is Hermes workspace pointing to AAA?
grep "workspace:" ~/.hermes/config.yaml
# If /root/.hermes/workspace → that's the AAA repo
```

## Step 2 — Sync Identity Files from AAA

```bash
for f in SOUL.md AGENTS.md IDENTITY.md USER.md MEMORY.md BOOTSTRAP.md HEARTBEAT.md; do
  cp /root/AAA/$f /root/.hermes/workspace/$f
done
cp /root/AAA/arifos.init /root/.hermes/workspace/arifos.init
cp /root/AAA/ROOT_CANON.yaml /root/.hermes/workspace/ROOT_CANON.yaml
```

## Step 3 — Fix config.yaml

```yaml
# Role — NOT asi-judge (ASI is arifOS kernel authority)
agent:
  role: hermes-agent   # was: asi-judge

# Enable cron
cron:
  enabled: true         # was: false

# Wire MCP servers
mcp:
  servers:
    arifosmcp:
      name: arifosmcp
      url: http://127.0.0.1:8080
      transport: streamable-http
      timeout: 30
    geoxmcp:
      name: geoxmcp
      url: http://127.0.0.1:8081
      transport: streamable-http
      timeout: 30

# Connect AAA skills
skills:
  external_dirs:
    - /root/AAA/skills
    - /root/.hermes/skills
```

Verify arifOS MCP is live:
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/health
# Expect: 200
```

## Step 4 — Create arifos SKILL.md Root

If `~/.hermes/skills/arifos/SKILL.md` doesn't exist:
```bash
cat > ~/.hermes/skills/arifos/SKILL.md << 'EOF'
---
name: arifos
description: arifOS Constitutional Governance — F1–F13 floors, SEAL/SABAR/VOID verdicts, VAULT999 ledger, session boot sequence.
category: governance
version: 1.0.0
---

# arifOS Skill Bundle

## Skills
- arifos-agent-output-templates
- arifos-fastmcp-tool-registration-fix
- arifos-three-surface-audit
- arifos-f1-f13-governance-impl.md
- arifos-container-patch-workflow.md

## Boot Sequence (per AGENTS.md)
1. ROOT_CANON.yaml
2. SOUL.md
3. USER.md
4. arifos.init
5. memory/YYYY-MM-DD.md

## Verdict System
- SEAL = safe to proceed
- SABAR = proceed with warning
- HOLD = pause for human review
- VOID = rejected by F9 Anti-Hantu
EOF
```

## Step 5 — Register Hermes in AAA Agent Registry

Add to `/root/AAA/registries/agents.yaml`:
```yaml
  - id: hermes-asi
    name: Hermes ASI
    role: hermes-agent
    intelligence_tier: APEX
    risk_tier: low
    authority_level: execute
    approval_policy: auto
    host_binding: hermes-agent
    allowed_servers:
      - arifosmcp
      - geoxmcp
    required_witnesses:
      - ARIFOS
      - HUMAN
```

Validate YAML:
```bash
python3 -c "import yaml; yaml.safe_load(open('/root/AAA/registries/agents.yaml')); print('YAML valid')"
```

Commit:
```bash
cd /root/AAA && git add registries/agents.yaml
git commit -m "🪙 REGISTRY: Add hermes-asi agent record"
git pull --rebase origin main  # handle divergence
git push origin main
```

## Step 6 — Create Agent Record and Observability

```bash
# Agent record
cat > /root/AAA/agents/hermes-asi/agent-record.json << 'EOF'
{
  "id": "hermes-asi",
  "workspace_path": "/root/.hermes/workspace",
  "config_path": "/root/.hermes/config.yaml",
  "memory_path": "/root/.hermes/memories",
  "backup_schedule": "daily 05:00 MYT",
  "mcp_servers": [
    {"name": "arifosmcp", "url": "http://127.0.0.1:8080"},
    {"name": "geoxmcp", "url": "http://127.0.0.1:8081"}
  ]
}
EOF
```

**IMPORTANT — Observability dir naming:**
- Directory name `hermes/` COLLIDES with `.gitignore` pattern `hermes/`
- Use `observability/hermes-gateway/` NOT `observability/hermes/`
- Any dir matching a `.gitignore` pattern will silently fail `git add`

## Step 7 — Gitignore Hygiene

Add to `/root/AAA/.gitignore`:
```
# Backup snapshots (contain embedded git repos — can't commit these)
hermes-backup/daily/

# Live mirror
hermes/
```

**Caution:** The pattern `hermes/` matches `observability/hermes/` too.
Rename observability dirs to avoid collision: `hermes-gateway/`, `hermes-observability/`, etc.

## Step 8 — Backup Cron

Create Hermes cron job (fires at 21:00 UTC = 5AM MYT):
```bash
hermes cron create \
  --name "Hermes → AAA Daily Backup" \
  --schedule "0 21 * * *" \
  --repeat forever \
  --deliver origin \
  --prompt "Backup ~/.hermes/workspace, memories, skills, config to /root/AAA/hermes-backup/daily/"
```

Or use the existing backup script:
```bash
/root/AAA/hermes-backup/backup-hermes.sh
```
Verify it's in the cron job list:
```bash
hermes cron list
```

## Step 9 — Commit Everything

```bash
cd /root/AAA
git add agents/hermes-asi/ observability/hermes-gateway/ .gitignore
git commit -m "🪙 AGENT: Add hermes-asi agent record + observability"
git push origin main
```

---

## Verification Checklist

| Check | Command |
|-------|---------|
| arifOS MCP live | `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/health` → 200 |
| Config role | `grep "role:" ~/.hermes/config.yaml` → `hermes-agent` |
| Cron enabled | `grep "enabled:" ~/.hermes/config.yaml | grep cron` → true |
| Skills external_dirs | `grep -A2 "external_dirs:" ~/.hermes/config.yaml` → /root/AAA/skills |
| AAA registry valid | `python3 -c "import yaml; yaml.safe_load(open('/root/AAA/registries/agents.yaml'))"` |
| Cron job scheduled | `hermes cron list` → job ID present |
| Restart needed | Hermes config changes require `hermes restart` |

---

## Common Failures

### `git add` silently fails — file not tracked
**Cause:** `.gitignore` pattern matching directory name.
**Fix:** `ls -la observability/` — if `hermes/` exists, rename to `hermes-gateway/`.

### Backup snapshot has embedded git repo
**Cause:** `~/.hermes/workspace/` IS a git repo (AAA). Copying it as a directory inside AAA creates an embedded repo.
**Fix:** Add `hermes-backup/daily/` to `.gitignore`. Commit only the backup script and config, not the snapshot dirs.

### Push rejected — divergent branches
**Fix:**
```bash
git stash
git pull --rebase origin main
git stash pop
git push origin main
```

### YAML invalid after patch
**Fix:** Always validate after editing:
```bash
python3 -c "import yaml; yaml.safe_load(open('/root/AAA/registries/agents.yaml')); print('valid')"
```
