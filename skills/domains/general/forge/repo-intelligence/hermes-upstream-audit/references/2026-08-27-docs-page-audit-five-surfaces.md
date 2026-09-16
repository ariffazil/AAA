# Docs-Page Audit — Five Surfaces (2026-08-27)

Session record: Arif pasted five upstream Hermes docs pages sequentially
(deliverable mode, integrations, credential pools, skills usage, skills hub URL,
tool search). Each was audited against the live box (v0.20.1, +2 carried
commits) rather than summarized. Pattern holds: box at-par or ahead on every
surface; every genuine finding was internal drift, not missing upstream
features.

## Per-surface verdicts

| Page | Box state | Evidence |
|---|---|---|
| Deliverable mode | VERIFIED + patched | `MEDIA_DELIVERY_EXTS` single-source tuple at `gateway/platforms/base.py:1893`; `extract_local_files()` bare-path pickup with code-span masking; `kanban_tools.py:683` artifacts param. Silent-fail trap: paths mentioned but not on disk are dropped with only a gateway.log line. |
| Integrations | AHEAD (deliberate divergence) | FED-primary model doctrine (config `_note` F13 2026-08-09); `web.backend: searxng` for search+extract (upstream default firecrawl; SearXNG extract works via `web_search_registry.py` fallthrough); TTS `i-arif-sovereign` command provider (2-stage MiniMax + DSP pipeline, not in docs); Honcho memory hybrid active; 4 governance plugins (mcp-health-gate, model_picker_gate, seal-command, seal-queue). |
| Credential pools | DORMANT by architecture | 17 providers × 1 key each, zero multi-key pools, no `credential_pool_strategies` (fill_first default). Rotation logic verified in `agent/credential_pool.py` (150KB) but with one key there is nothing to rotate. Redundancy solved at federation layer (FED :4000 + cross-provider fallback), not key layer. Finding: xiaomi/MiMo token-plan key status `exhausted` (needs renewal before MiMo voice lane use). Env keys never persisted in auth.json — fingerprint only. `~/.claude/.credentials.json` auto-seeds the anthropic pool (confirmed working). |
| Skills usage | AHEAD + needed sweep | `skills.external_dirs` points at organ repos (`/root/AAA/skills`, `GEOX`, `WEALTH`, `WELL`) — skills live in git-versioned organ repos, beyond docs pattern. But catalog had grown 303 local SKILL.md + ~150 more via external dirs = 476 total vs doctrine's "147 is already too many". |
| Skills hub URL | 99.8% sovereign | 384 local + 69 builtin + **1** hub-installed (`har-derived-api-client`) of 90,700 hub skills. Discovery: fork's carried commits polluted the install tree with federation skills → builtin/local overlap. |
| Tool search | ACTIVE + tuned past default | `enabled: auto`, `threshold_pct: 10` (default 5), `max_search_limit: 20` (default 25). Session itself ran at tier 1: 14 MCP servers deferred (~250 tools), core tools eager, manifest visible. `tool_search`/`tool_call` exercised live during the session. |

## Findings executed (on "ok compile all task and execute all")

1. **STT drift fixed:** config said `stt.provider: openai, whisper-1` while
   SOUL.md doctrine says Groq whisper-large-v3-turbo. Patched via yaml
   roundtrip → `stt.provider: groq`, `stt.groq.model: whisper-large-v3-turbo`.
2. **Artifact-bias personality patch** (from deliverable-mode page): appended
   "Deliverable bias on gateway lanes" block to `agent.personalities.xray` —
   chart for data, PDF for reports, verify-on-disk-before-mentioning-path,
   CLI stays text-first.
3. **Skill sweep 303 → 191:** 71 dirs quarantined (identical-or-stale vs a
   live copy elsewhere) + 29 dead `_drafts` (generic "Reusable
   capability/workflow discovered" auto-minted by a leaky ephemeral-genesis
   pipeline). Snapshot: `/root/forge_work/_quarantine/skills-sweep-snapshot-20260827-030604/`
   (7-day grace). Quarantine: `.../skills-sweep-removed-20260827/`.
4. **Gateway restarted** via `systemctl restart hermes-asi-gateway.service`
   → new PID, both patches live, Telegram poller reconnecting.

## Incidents survived (encoded as pitfalls 12–15 in SKILL.md)

- YAML string-surgery broke parsing; first recovery restored a WRONG (older)
  backup → 3 minutes of state regression (21 MCP servers missing) until
  structural re-validation caught it. Roundtrip-only from now on.
- Sweep script quarantined 0 dirs on first run twice: (a) Path.resolve()
  followed symlinks out of the scope filter; (b) classification rebuilt
  correctly but filter still rejected. Verbose-filter debugging found it.
- The keep-side rule that finally worked: local dirs with NEWER mtime than the
  install-tree twin are the live version (68 kept); byte-identical or
  older-than-install local copies are safe to quarantine (73 + 29 drafts).

## Left open (not executed — needs F13 or future session)

- `hermes gateway install --force` to regenerate systemd unit
  (TimeoutStopSec=90s < drain_timeout=180s SIGKILL risk).
- 68 kept-local skills are newer than install tree → fork skill content is
  evolving faster than upstream; watch for name/merge drift on next update.
- xiaomi/MiMo exhausted key renewal if MiMo voicedesign lane is needed.
