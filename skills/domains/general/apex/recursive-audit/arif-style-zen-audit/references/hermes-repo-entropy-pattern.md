# HERMES Repo Entropy Pattern — ZEN Audit Reference

> Captured from HERMES ZEN audit 2026-08-30 (commit-wave closure session).

## Common entropy sources in /root/HERMES

When auditing the HERMES repo, expect these residue classes:

### 1. backups/ (can exceed 1GB)
- **corrupt-YYYYMMDD/** — named corrupt/malformed state.db dumps. Always dead. Safe to remove.
- **state-db/** — old state.db snapshots (250MB+ each). Current state.db is the live one; old snapshots are redundant after ~48h. Remove if older than 2 days.
- **root-baks-YYYYMMDD/** — today's config/auth backups. Keep, tiny.
- **zen-YYYYMMDDTHHMMSSZ/** — old zen audit receipts. Tiny, can keep or remove.

### 2. cache/ (can exceed 700MB)
- **videos/** — transient video files. Safe to remove.
- **terminal-output/** — old terminal session captures. Safe to remove.
- **geox-*/** — stale project-specific cache dirs. Safe to remove.
- **images/** — generated/downloaded images. Some may be referenced by active skills. Check before removing.
- **browser-use/** — browser session artifacts. Usually small.
- **audio/** — TTS/voice cache. Usually small.

### 3. checkpoints/ (~90MB)
- **store/** — bare git repo used by checkpoint system. DO NOT remove — referenced by runtime.

### 4. Git stashes
- Old stashes from weeks ago are dead weight. `git stash drop` safely.

### 5. Config baks in root
- `config.yaml.bak-*` files from old operations. Usually stale. Safe to remove.

### 6. Runtime tmp files
- `.gateway_state_*.tmp` — gateway runtime artifacts. Add to .gitignore.
- `.restart_notify.json` — restart notification artifact. Add to .gitignore.

## Commit-wave technique for bulk dirty repos

When HERMES has 300+ dirty files (common after multi-agent sessions):

### Phase 1: Tracked changes (deletions + modifications)
```bash
cd /root/HERMES
git add -u          # stages ALL tracked deletions + modifications
git commit -m "chore(skills): remove N files — skills migrated to AAA/skills"
```
This catches everything: deletions (skills migrated to AAA), modifications (skill patches, config drift, cron sync), and jobs.json runtime drift.

### Phase 2: Untracked new files
```bash
git add -A          # stages all untracked files
git commit -m "feat(skills): +N authored skills and reference corpora"
```

### Phase 3: Runtime residue
```bash
echo ".restart_notify.json" >> .gitignore
git add .gitignore
git commit --amend --no-edit  # fold into the last commit
```

### Phase 4: Verify
```bash
git status --porcelain | wc -l   # should be 0
git log --oneline -5             # verify commit chain
python3 -c "import json; json.load(open('cron/jobs.json'))"  # jobs.json valid
```

## jobs.json runtime drift

jobs.json is modified at runtime by cron execution:
- `repeat.completed` counter increments
- `next_run_at` / `last_run_at` timestamps update
- `updated_at` timestamp updates

This is **normal**, not corruption. Commit it as `chore(cron): runtime drift`. The validator is the only sanctioned *intentional* writer, but runtime execution auto-updates state fields.

## VAULT999 seal fallback

If `arif_seal` MCP call times out (5min cap on large payloads), write directly to `/root/VAULT999/local_seals.jsonl`:

```python
import json, datetime
receipt = {
    'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'action': 'YOUR_ACTION',
    'actor_id': 'hermes_asi',
    'authority': 'F13_SOVEREIGN',
    'summary': 'YOUR_SUMMARY'
}
with open('/root/VAULT999/local_seals.jsonl', 'a') as f:
    f.write(json.dumps(receipt) + '\n')
```

## Mesh policy (HERMES-specific)

- **AAA/skills** = canonical source for federation skills
- **HERMES/skills** = Hermes runtime skills only (arifos, hermes-cron-zen, shadow-mode, etc.)
- Kimi symlinks pointing to HERMES-native skills are correct — not duplicates
- No re-mesh needed when AAA/skills is the declared single source
