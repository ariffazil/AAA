# state.db Usage Evidence — Measure Real Skill Usage Before Any Zen/Prune Decision

Proven 2026-08-25 against a live install (512 SKILL.md indexed, 35,411 messages,
327 sessions/30d). This is the LIVE-surface usage measurement the
falsify-before-prune rule requires — it replaces guesswork and category shape
with per-skill traffic data.

## Why this matters

Progressive disclosure means a skill costs ~nothing at Level 2 (loaded on
demand) — but EVERY indexed skill pays Level 0 rent: its name+description
frontmatter is injected into the system prompt of EVERY session. A 512-skill
library measured 272KB of frontmatter ≈ 68K tokens per session (~20× a normal
~3K-token install). Only 131 of those 512 skills were actually loaded via
skill_view in 30 days — 75% pure dead weight paying rent.

## Measurement 1 — which skills are actually used (skill_view traffic)

```python
import sqlite3, json, collections
db = sqlite3.connect('file:/root/.hermes/state.db?mode=ro', uri=True)
cur = db.cursor()
# messages.tool_name holds the tool; content holds the JSON args
cur.execute("""SELECT content FROM messages
               WHERE tool_name='skill_view'
               AND timestamp > strftime('%s','now','-30 days')""")
calls = collections.Counter()
for (c,) in cur.fetchall():
    try:
        name = json.loads(c).get('name')
        if name: calls[name] += 1
    except Exception: pass
# keep-set = keys of calls + constitutional/ops core; everything else is
# cold-storage candidate
```

Key columns: `messages(id, session_id, role, content, tool_call_id, tool_calls,
tool_name, timestamp, ...)`. Parse `content` as JSON for the `name` arg.

Also count `tool_name='skill_manage'` — that's skill WRITE traffic (creation/
patch activity), useful to spot recently-forged skills that haven't had time
to accumulate view traffic.

## Measurement 2 — the aggregate bill (session tokens + cache)

```sql
SELECT COUNT(*), SUM(input_tokens), SUM(output_tokens),
       SUM(cache_read_tokens), SUM(estimated_cost_usd)
FROM sessions WHERE started_at > strftime('%s','now','-30 days');
```

`cache_read_tokens > input_tokens` is NORMAL and expected (system prompt is
cache-re-read every turn — observed 1314%). The real costs of an oversized
index are NOT dollars (cache is cheap — $1.26/month observed): they are
(1) context window fills faster → compression triggers earlier → conversation
memory lost sooner; (2) skill selection accuracy degrades navigating 500
entries.

## Measurement 3 — index weight per category (prompt-cost proxy)

```bash
# frontmatter bytes per top-dir = approximate Level-0 prompt cost
for d in /root/.hermes/skills/*/; do
  b=$(find "$d" -name 'SKILL.md' -exec awk '/^---$/{n++; next} n==1' {} \; 2>/dev/null | wc -c)
  [ "$b" -gt 0 ] && echo "$b $(basename $d)"
done | sort -rn
```

⚠️ Count SKILL.md at UNLIMITED depth (`find ... -name SKILL.md | wc -l`) —
`-maxdepth 2` misses nested category dirs and undercounts (207 vs 512 real).

## The zen lever — cold storage, NOT external_dirs

CRITICAL distinction proven this session:

- Moving a skill to `skills.external_dirs` does NOT zen the prompt — external
  skills appear in the system prompt index identically to local ones
  (documented Hermes behavior; confirmed in the skills docs).
- The only true Level-0 deload is moving the skill OUT of all scanned paths
  (e.g. `/root/.hermes/skills-cold/`) with a manifest for one-command thaw:
  `mv` back + `/reload_skills`. Fully reversible (F1), no restart needed.

Cold-storage runbook: write manifest (path, name, hash, last-used) → `mv`
skill dirs to cold dir → `/reload_skills` → verify index count dropped.
Thaw: `mv` back + `/reload_skills`. Slash commands for cold skills vanish
until thawed — surface that trade-off to the sovereign before executing.

## Canonical Hermes mechanisms verified this session

- `hermes skills opt-out` + `.no-bundled-skills` marker — stops update
  re-seeding for a profile (curator can't keep up otherwise).
- `mcp_servers.<name>.enabled: false` + `tools.include/exclude` (glob-capable)
  — MCP diet; `/reload_mcp` applies without restart.
- Profiles ARE the partition primitive (Bot Mode = UI over profiles) — but a
  gateway runs ONE profile; other profiles' skills dirs are disk-clutter only,
  not prompt cost. Diet the profile the gateway actually runs.
- Curator settings (`curator.interval_hours/archive_after_days`) can't outrun
  unbounded seeding — pair with usage-evidence cold storage + a recurring
  60-day-idle sweep.

## Session evidence snapshot (2026-08-25, default profile)

- 512 SKILL.md on disk / ~533 banner count (banner counts bundles) — only 131
  loaded in 30d. Top traffic: shadow-mode, nusantara-voice-stack,
  mulerouter-media, sinboy-shadow-lane, token-plan-* (voice/media lane).
- 8 duplicate-name skills (know-math/-physics/-language, forge-vss-parser,
  arifOS, FORGE-sct-federation-ingress, APEX, token-plan-image).
- `.archive-2026-08-15` (nasi-lemak) still scanned → archives under skills/
  still pay index rent; move archives OUT of the scanned tree.
- MCP: 247 tools across servers; aforge alone 114; stdio servers
  (github/firecrawl/hermes/mage/notebooklm) stuck "connecting" at boot.
- Heavy dirs by disk: capital/ 8.1MB, geology/ 3.8MB (mostly non-SKILL.md
  payload — disk cost, not prompt cost).
