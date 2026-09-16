# Runtime probe cookbook

One-shot command set for a Hermes runtime audit. Run in this order — each step's output decides whether
the next one is worth running. Nothing here mutates anything unless marked MUTATING.

## 1. Identity and version

```bash
hermes --version                       # upstream sha, local sha, carried commits
hostname; nproc; free -g | head -2; df -h / | tail -1
ls -la ~/.hermes/ | head -40
du -sh ~/.hermes/* 2>/dev/null | sort -h | tail -25
```

## 2. Prompt tax

```bash
hermes prompt-size
hermes prompt-size --json > /tmp/prompt-size.json
```

What to extract:

- system prompt total, and the three tiers (stable / context / volatile)
- skills-index bytes, memory bytes, user-profile bytes
- tool-schema bytes and the tool count
- top skills by SKILL.md size **and** by index cost (separate rankings — they disagree)

Convert the index to tokens (`bytes / 4`) and state it as a per-turn cost.

## 3. Context contract reconciliation

```bash
grep -nE 'context_length' ~/.hermes/config.yaml

# the harness process environment (NOT the CLI's)
tr '\0' '\n' < /proc/$(pgrep -f 'gateway run' | head -1)/environ \
  | grep -iE 'BASE_URL|API_BASE|OPENAI|HERMES_'

# who owns each hop
ss -ltnp | grep -E ':(4010|4012|4013|4000|7074)\b'

# the clamp constant in whatever sits in front
grep -rnE 'MAX_BODY|GUARD|413|body_bytes' <middleware-source>.py | head

# what the upstream actually advertises
curl -s http://127.0.0.1:<fed-port>/v1/models/<model> | head -c 400
```

Build the ledger explicitly: harness value / proxy clamp (bytes ÷ 4 ≈ tokens) / upstream registry value.
The smallest wins. If the harness value is the largest, its compressor never fires — that is the finding.

Also check whether the clamp has ever logged a drop:
`journalctl -u <middleware> --since '14 days ago' | grep -c 'guard'`.
Zero hits over two weeks is unresolved (unused, or unlogged), not clean.

## 4. Storage attribution

```bash
ls -la ~/.hermes/state.db*
hermes doctor | sed -n '/SQLite/,/^$/p'
hermes sessions stats

du -sh ~/.hermes/{sessions,workspace,logs,cache,pastes,output,artifacts,state-snapshots,plugins} 2>/dev/null
find ~/.hermes/logs -type f -size +20M | head
```

Table-level attribution:

```bash
python3 - <<'PY'
import sqlite3
c = sqlite3.connect('/root/.hermes/state.db')
for name, mb in c.execute(
    'select name, sum(pgsize)/1048576.0 m from dbstat group by name order by m desc limit 15'):
    print('%-34s %8.1f MB' % (name, mb))
print('sessions:', c.execute('select count(*) from sessions').fetchone()[0])
print('messages:', c.execute('select count(*) from messages').fetchone()[0])
print('unclosed:', c.execute('select count(*) from sessions where ended_at is null').fetchone()[0])
print('last 7d:', c.execute(
    "select count(*) from sessions where started_at > strftime('%s','now','-7 days')").fetchone()[0])
PY
```

Maintenance (MUTATING — gate it, and quiesce the gateway for a clean VACUUM):

```bash
hermes sessions optimize-storage
hermes sessions optimize
hermes sessions prune --help
hermes sessions archive --help
```

## 5. Surface inventory

```bash
hermes doctor
hermes status
hermes curator status
hermes memory status
hermes mcp list

python3 - <<'PY'
import json, collections
jobs = json.load(open('/root/.hermes/cron/jobs.json'))['jobs']
print('jobs:', len(jobs), 'enabled:', sum(1 for j in jobs if j.get('enabled')))
print('deliver targets:', collections.Counter(str(j.get('deliver')) for j in jobs).most_common(6))
print('last_status:', collections.Counter(str(j.get('last_status')) for j in jobs).most_common())
PY
```

## 6. Directory sprawl

```bash
ls -d ~/.hermes/*/ | tr '\n' ' '; echo
for d in ~/.hermes/*/; do
  printf '%-24s %5s files  %8s\n' "$(basename $d)" "$(find $d -type f 2>/dev/null | wc -l)" "$(du -sh $d 2>/dev/null | cut -f1)"
done
```

## 7. Secret modes

```bash
for f in $(grep -rlE '(API_KEY|TOKEN|SECRET|PASSWORD|_KEY)=[^$]' /etc/systemd/system/ 2>/dev/null); do
  p=$(stat -c '%a' "$f"); [ "$p" != "600" ] && echo "OPEN $p $f"
done
ls -la ~/.hermes/.env*
chmod 600 <each flagged file>        # fix, then re-run the sweep to prove it
```

## 8. Process-layer sprawl

```
ls /etc/systemd/system/<unit>.service.d/
systemctl cat <unit>.service | head -60      # base unit + every drop-in, in load order
systemctl show <unit> -p ActiveEnterTimestamp -p NRestarts
```

## 9. Re-measure

After any fix, run §2, §4 and `df -h /` again and record the delta. An audit without a second reading has
no evidence the change landed.
