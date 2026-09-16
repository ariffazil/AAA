# Skill-Federation Unification Receipt Audit — 2026-08-21

Worked example for the "Unification / Canonicalization Receipt Audit" section of
live-probe-audit-pattern. Subject: commit `dad36371` (kimi-code/FI-008) claiming the
federation skill estate was consolidated to "one form, one source of truth
(/root/AAA/skills)".

## The receipt's claims vs live state

| Claim | Live probe result | Verdict |
|---|---|---|
| Claude/Codex/Grok = symlink → AAA | 3/3 dirs are full symlinks to /root/AAA/skills, zero physical | ✅ CONFIRMED |
| OpenCode = curated, bounded | 5 physical + 7 symlinks in /root/.config/opencode/skills | ✅ CONFIRMED |
| Kimi reads AAA directly | /root/.kimi-code/config.toml line 3: `extra_skill_dirs=["/root/AAA/skills"]`, `.agents` double-list removed | ✅ CONFIRMED |
| 185 mirrors quarantined | MANIFEST 187 lines; quarantine-20260821 holds 192 dirs | ✅ CONFIRMED (rounding) |
| `agent:kimi` target dead + F13 note | script exits 1 with doctrine note | ✅ CONFIRMED |
| Kimi "0 physical copies" | Live lane clean (19 physical), but DEAD lane /root/.kimi (→ /root/.arifos/agents/kimi) still holds 146 stale physical copies | ⚠️ HALF-TRUE (residue) |
| Hermes row: "AAA is the canonical source" | INVERTED: 88 symlinks inside AAA/skills point to /root/HERMES/skills (502 SKILL.md); .hermes/skills has 241 physical, 124 diverged from AAA, 111 runtime-newer | ❌ FALSE (inverted) |
| "One source of truth" | Three physical stores: .hermes/skills (241) + HERMES/skills (502) + AAA/skills (198 real + 96 symlinks) | ❌ FALSE |
| "9 commits today" | git log --since=local-midnight = 14 (report counted only own agent's commits) | 📊 UNDERCOUNT |
| "42 agents clean" | 33 active cards / 39 agent dirs / 19 registry entries — no surface reproduces 42 | 📊 NOT REPRODUCIBLE |
| "Gateway stable" | hermes-asi-gateway running; but arif-dream.service in auto-restart loop | ⚠️ PARTIAL |

## Probe commands that produced each number

```bash
# Triclass census per harness dir
for p in /root/.claude/skills /root/.codex/skills /root/.grok/skills \
         /root/.kimi/skills /root/.kimi-code/skills /root/.hermes/skills; do
  echo "$p: real=$(find $p -maxdepth 1 -type d ! -path $p | wc -l) links=$(find $p -maxdepth 1 -type l | wc -l) files=$(find $p -maxdepth 1 -type f | wc -l)"
done

# Canonicality inversion census (inside claimed canonical)
python3 - <<'EOF'
from collections import Counter
import os
tgts = Counter()
for e in os.listdir('/root/AAA/skills'):
    p = f'/root/AAA/skills/{e}'
    if os.path.islink(p):
        t = os.readlink(p)
        tgts['SELF' if '/root/AAA/skills' in t else '/'.join(t.strip('/').split('/')[:2])] += 1
print(tgts)   # → {'root/HERMES': 88, 'root/AAA': 8}
EOF

# Dead-lane discovery (readlink chain + last session mtime)
readlink -f /root/.kimi            # → /root/.arifos/agents/kimi
ls -t /root/.kimi/sessions | head -1; stat -c '%y' /root/.kimi/sessions/$(ls -t /root/.kimi/sessions | head -1)
ls -t /root/.kimi-code/sessions | head -1   # live lane, newest session

# Divergence + direction census between two physical stores
python3 - <<'EOF'
import os
A = {e for e in os.listdir('/root/.hermes/skills') if not os.path.islink(f'/root/.hermes/skills/{e}')}
B = {e for e in os.listdir('/root/AAA/skills') if os.path.isdir(f'/root/AAA/skills/{e}')}
ident = diff = an = bn = 0
for n in A & B:
    a, b = f'/root/.hermes/skills/{n}/SKILL.md', f'/root/AAA/skills/{n}/SKILL.md'
    if os.path.isfile(a) and os.path.isfile(b):
        if open(a,'rb').read() == open(b,'rb').read(): ident += 1
        else:
            diff += 1
            if os.path.getmtime(a) > os.path.getmtime(b): an += 1
            else: bn += 1
print(f'shared={len(A&B)} identical={ident} diverged={diff} runtime-newer={an} canonical-newer={bn}')
EOF

# Headline recount from its own surface
git -C /root/AAA log --since='2026-08-21 00:00:00 +0800' --oneline | wc -l   # 14, not 9
find /root/AAA/agents -name agent-card.json | grep -v '_superseded\|_archive' | wc -l  # 33
```

## Estate topology discovered (the receipt's hidden truth)

- `/root/AAA/skills` — 330 entries: 198 real dirs + 96 symlinks (88 → /root/HERMES/skills, 8 self)
- `/root/.hermes/skills` — 294 entries: 241 real + 46 symlinks (→ .agents/skills which is itself → AAA/skills)
- `/root/HERMES/skills` — git-tracked store, 502 SKILL.md, the ACTUAL upstream for 88 AAA entries
- `/root/.kimi-code/skills` — live kimi lane: 16 real dirs (19 physical SKILL.md) + 94 symlinks + 40 registry JSON files
- `/root/.kimi` → `/root/.arifos/agents/kimi` — dead lane, 146 stale physical copies, last session 2026-08-14
- `/root/.agents/skills` → `/root/AAA/skills` (full symlink; listing it always equals AAA)

## Key lessons

1. "Single source of truth" claims must be probed INSIDE the claimed canonical — symlink target census by root exposes inversion in one command.
2. A harness with multiple historical homes (.kimi vs .kimi-code) means "zero copies" must be verified against EVERY home, not just the live one.
3. Divergence direction matters more than divergence count: copies newer than canonical = active drift, not cosmetic.
4. Undercounts happen too — recount, never assume inflation direction.
5. Verify `.bak` config files are excluded when probing live config (three .bak files carried the OLD extra_skill_dirs value).
