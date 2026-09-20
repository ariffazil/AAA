# MCP Server Zen — Pattern (PROVEN 2026-08-27, 6 servers removed)

> **Provenance:** Phase 2 of Hermes Zen operation. Skill collapse → MCP prune (Arif's "MCP last" sequencing doctrine). 21 → 15 servers, 6 disabled+uncalled removed.

## When to Use

After skill collapse phase (or instead of it if the library is healthy but MCP config has dead weight). Apply this protocol when:

- The user asks to "clean MCP", "audit MCP", "remove dead servers", "zen MCP"
- `mcp_servers` block in `config.yaml` is >15 entries
- Banner shows many "configured" + "disabled" servers
- `mcp__*` tool calls in session DB cluster around <10 servers despite 20+ configured

## Phase A — Inventory (111 SENSE)

You cannot zen what you have not counted. **Do not trust the banner** (it shows transport + status, not firing data).

### A.1 — Read config

```python
import yaml
with open("/root/.hermes/config.yaml") as f:
    c = yaml.safe_load(f)
mcp = c.get("mcp_servers", {})
print(f"Total: {len(mcp)}")
for name, s in mcp.items():
    url = s.get("url", s.get("httpUrl", s.get("command", "?")))
    enabled = not s.get("disabled", False) and s.get("enabled", True)
    print(f"  {name:25} {'ENABLED' if enabled else 'DISABLED':10}  {url}")
```

### A.2 — Pull firing data from session DB

The signal-of-truth is the actual `mcp__*` tool names in `/root/HERMES/state.db`:

```sql
SELECT tool_name, COUNT(*) FROM messages
WHERE tool_name LIKE 'mcp__%'
GROUP BY tool_name ORDER BY 2 DESC;
```

Group by server prefix:
```python
import re, sqlite3
from collections import defaultdict
conn = sqlite3.connect("/root/HERMES/state.db")
c = conn.cursor()
c.execute("SELECT tool_name, COUNT(*) FROM messages WHERE tool_name LIKE 'mcp__%' GROUP BY tool_name")
totals = defaultdict(int)
for name, cnt in c.fetchall():
    m = re.match(r"mcp__([a-zA-Z0-9_-]+)__", name)
    if m:
        totals[m.group(1)] += cnt
conn.close()
for srv, cnt in sorted(totals.items(), key=lambda x: -x[1]):
    print(f"{cnt:5d}  {srv}")
```

**Servers with 0 calls in DB = "configured + unfired" candidate.** Servers with 0 calls AND `disabled: true` in config = pure dead weight, REMOVE first.

### A.3 — Read the YAML `note:` field

Some servers are intentionally inert ("Wired but inert until TOKEN lands"). Do not remove these. Example from real config (2026-08-27):

```yaml
mapbox:
  enabled: true
  url: https://mcp.mapbox.com/mcp
  note: "Inert until MAPBOX_ACCESS_TOKEN lands in kunci-root.env"
```

These are future-state, not dead. **KEEP even with 0 calls.**

## Phase B — Falsify Arif's Redundancy Hypothesis (CRITICAL)

When Arif (or anyone) says "X is redundant, Y is redundant" — DO NOT execute. The hypothesis is a starting point, not a fact.

**Common false claims (proven 2026-08-27):**

| Claimed redundancy | Actual reality |
|---|---|
| Image-gen ×6 redundant | mage (Modal GPU, MS Mage-Flow) + minimax-media (MiniMax suite) + gemini-media (Google) = 3 different vendors. **Load-bearing** if one rate-limits. Not redundant — resilience pattern. |
| Search/scrape ×4 redundant | firecrawl (169 calls PRIMARY) + minimax web_search (12 calls FALLBACK) = primary + fallback (correct). social-mcp ≠ web search (X/Reddit signals). composio ≠ web search (OAuth API). All distinct roles. |
| Social ×3 redundant | social-mcp (X/Twitter + Reddit, X protocol) vs composio (Gmail OAuth + Reddit OAuth) = different auth model + different surfaces. Not redundant. |

**Rule:** "Looks like redundancy" → "Verify with firing data" → "Often turns out to be distinct roles". Don't act on hypothesis without falsification.

## Phase C — Decision Matrix

Per-server classification:

| Decision | Criteria | Action |
|---|---|---|
| KEEP-CRITICAL | Fires ≥10 calls AND belongs to federation organs (arifos/aforge/fed/geox/wealth/well) | Keep, must verify still connects |
| KEEP-PRIMARY | Fires ≥50 calls (firecrawl, social-mcp, arifos, minimax-media) | Keep, no further analysis |
| KEEP-FALLBACK | Fires <50 calls BUT distinct role from any other server | Keep (e.g., minimax web_search as firecrawl fallback) |
| KEEP-FUTURE | 0 calls AND YAML `note:` indicates "inert until token/credential lands" | Keep (intentional future-state wiring) |
| KEEP-INFRASTRUCTURE | 0 calls BUT Hermes-only orphan (may be infra for Claude/OpenCode/Qwen surfaces) | Keep (doctrine §Ghost Directory Pitfall) |
| **REMOVE** | `disabled: true` (or `enabled: false`) AND 0 calls in session DB AND no `note:` indicating future-state | Remove from config |

## Phase D — Execution (config.yaml edit)

### D.1 — Backup first (F1 reversibility)

```bash
cp /root/.hermes/config.yaml /root/.hermes/config.yaml.bak-pre-mcp-zen-YYYYMMDDTHHMMSSZ
```

### D.2 — Use ruamel.yaml (NOT yaml.dump)

`yaml.dump` re-flows the entire file, destroying all comments and key ordering. Use `ruamel.yaml` with `preserve_quotes=True`:

```python
from ruamel.yaml import YAML
ryaml = YAML()
ryaml.preserve_quotes = True

with open("/root/.hermes/config.yaml") as f:
    rconfig = ryaml.load(f)

REMOVE = ["deep-research", "github", "hermes", "hound", "notebooklm", "openrouter"]
for name in REMOVE:
    if name in rconfig.get("mcp_servers", {}):
        del rconfig["mcp_servers"][name]

with open("/root/.hermes/config.yaml", "w") as f:
    ryaml.dump(rconfig, f)
```

### D.3 — Verify

```python
import yaml
with open("/root/.hermes/config.yaml") as f:
    c = yaml.safe_load(f)
print(f"mcp_servers: {len(c.get('mcp_servers', {}))}")
# Confirm parseable, count drops to expected number
```

### D.4 — Write LEDGER

`/root/.hermes/skills/.archive-YYYY-MM-DD/MCP_ZEN_LEDGER_YYYY-MM-DD.md` with:

- Inventory before (21 servers)
- Firing data summary (480 calls across N servers)
- Decisions per server (KEEP / REMOVE with rationale)
- Falsification results (e.g., "Arif's image-gen redundancy hypothesis FALSIFIED — 3 distinct vendors")
- Files changed + backup path
- Revert command: `cp <backup_path> <config.yaml>`

## Phase E — Live Verification (DO NOT SKIP)

Config changes do NOT take effect until the gateway restarts. A running gateway keeps the old config in memory until reload.

### E.1 — Federation organ health (must be 200)

```bash
for port in 8088 7072 8081 18082 18083 7074 7073; do
    code=$(curl -sS --max-time 5 -o /dev/null -w "%{http_code}" http://127.0.0.1:$port/health 2>/dev/null || echo "000")
    echo ":$port → $code"
done
```

If `arifos-kernel :8088` or `geox :8081` returns 404 on `/health`, try `/mcp` instead — these organs expose MCP on `/mcp` not `/health`. Both HTTP200 on `/mcp` = healthy.

### E.2 — Live MCP list

```bash
qwen mcp list
```

OR via raw query if `qwen` not available:
```bash
# Will only show after gateway restart — not before
```

### E.3 — Gateway restart (T2, NOT T0)

The running gateway has the OLD config in memory. **Changes do not apply until restart.** This is a T2 action (announce, don't silently kill).

**DO NOT** run `hermes gateway restart` from inside the gateway process — the gateway refuses with "command or referenced script cannot restart or stop the gateway from inside the gateway process". Either:
- Run from a separate SSH/cron shell (not this session)
- Or wait for next session — gateway picks up on cold start

**Hardlink pitfall:** `/root/.hermes/config.yaml` and `/root/HERMES/config.yaml` are the SAME inode (hardlinked). Editing one updates both. Verify with `stat -c '%i' <both_files>` — same inode number = hardlinked.

## Phase F — Cross-Reference Safety Check

Before finalizing REMOVE list, check for orphan references that would break:

```bash.2
for srv in "${REMOVE[@]}"; do
    refs=$(grep -rl "$srv" /root/.hermes/skills/ /root/AAA/skills/ /root/.hermes/cron/ 2>/dev/null | wc -l)
    echo "$srv: $refs external refs"
done
```

**Critical distinction:** References to MCP server names (like `github`) often match SKILL NAMES with the same word (e.g., `github-pr-workflow` is a skill that doesn't exist anyway, pre-existing debt, NOT introduced by the prune). Cross-check whether the referenced name is an MCP server or a skill.

```python
import os
# If /root/AAA/skills/<name>/SKILL.md exists → it's a skill reference (safe)
# If not, and the word is just generic ("scripts", "github", etc.) → likely descriptive
```

## Phase G — Decision Threshold

**Conservative default: only REMOVE what's undeniably dead.** A server is undeniably dead when ALL of:

1. `disabled: true` (or `enabled: false`) in config
2. 0 calls in session DB
3. No YAML `note:` indicating future-state wiring
4. No skill's `related_skills:` frontmatter points to it (and the pointed-to entity doesn't exist as a skill — in which case it's pre-existing debt, not introduced by this prune)

If any criterion is ambiguous → KEEP. Tier-2 deferral applies.

## Phase H — Result Template (use this to write LEDGER)

```markdown
# MCP_ZEN_LEDGER_YYYY-MM-DD.md

**Date (UTC):** {ts}
**Operator:** Hermes (on instruction from Arif, "MCP last" doctrine)
**Doctrine:** skill-audit-methodology §archive-but-verify + F1 reversibility

## Inventory
- Total before: N servers
- Firing data: M total tool calls in session DB history
- Servers with 0 calls: K

## Removed (N — all DISABLED + 0 calls + no future-state note)
- server1 — reason
- server2 — reason
- ...

## Kept (M)
### Critical infrastructure (organ-bound)
### Media + creative (distinct vendor lanes)
### Map + provider fallback
### Future-state (intentionally inert)

## Redundancy falsification
Arif's hypothesis: "X is redundant with Y"
Verified: ACTUAL distinct roles are [Z, W, V]
Decision: KEEP all

## Files
- /root/.hermes/config.yaml: N → M servers
- Backup: /root/.hermes/config.yaml.bak-pre-mcp-zen-{ts}

## Revert
`cp <backup_path> /root/.hermes/config.yaml`
```

## Pitfalls (specific to MCP prune)

- **Generic-name grep false positives.** `grep -c "github"` returns high counts because `github-pr-workflow` etc. exist as skill names. Always verify the referenced entity actually exists as a skill (check `/root/AAA/skills/<name>/SKILL.md`).
- **Config hardlink trap.** `/root/.hermes/config.yaml` and `/root/HERMES/config.yaml` are the same inode. Edit one, verify with `stat -c '%i'` both. Don't think you need to edit both — they're literally the same file.
- **Gateway doesn't auto-reload.** Config changes are dead letters until gateway restart. T2 action — announce, don't silently kill. From inside the gateway process, restart is refused; must use external shell or wait for next session.
- **Banner counts lie.** Hermes startup banner truncates server list. Always re-count with `len(c.get('mcp_servers', {}))` after reading config. Banner showed "7 visible" but actual count was 21 (14 disabled, hidden from banner).
- **`yaml.dump` destroys comments.** Use `ruamel.yaml` with `preserve_quotes=True`. The voice-config skill already proved this in 2026-08-18.
- **Don't remove "future-state" servers.** `note: "Inert until TOKEN lands"` = intentional future-state wiring, NOT dead weight. Keep.
- **Don't conflate "0 calls in DB" with "never used".** Session DB only captures the active Hermes session. Skills may be loaded by other agents (Claude Code, OpenCode, Codex, Qwen). The doctrine §Ghost Directory Pitfall applies — only remove what's `disabled: true` AND 0 calls AND no note.

## Session Result (2026-08-27, PROVEN)

- Removed 6 servers: `deep-research`, `github`, `hermes` (self-loop recursion risk), `hound`, `notebooklm`, `openrouter`
- All 6 satisfied triple criterion: `disabled: true` AND 0 calls AND no future-state note
- Config: 21 → 15 servers
- File size: 60,988 → 58,265 bytes (-2,723)
- Federation intact: 7/7 organs HTTP 200
- 2 redundancies hypothesized by Arif were FALSIFIED with evidence (mage+minimax-media+gemini-media = distinct vendors; social-mcp vs composio = different auth model)
- 0 reference breakage

## When to STOP — don't keep going

If after Phase A inventory:
- All "disabled" servers already removed
- All "0 calls + disabled" candidates gone
- Remaining 0-calls servers have `note:` or are Hermes-only orphans

**Stop.** Tier-2 (Hermes-only orphan) deferral applies. Move on to MCP server health, or finish.

If you find yourself saying "this one looks suspicious, let me check it" — that's the loop. **Trust the firing data, not your instinct.** The whole point of MCP prune is removing what the data says is dead, not what your gut says is suspicious.