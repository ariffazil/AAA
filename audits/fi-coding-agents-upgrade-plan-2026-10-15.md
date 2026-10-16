# FI Coding Agents — Upgrade & Evolution Plan

Forged 2026-10-15 · kimi-code / FI-008 · KVM8 · after the FI-002 shadow audit
Companion to `claude-code-shadow-2026-10-15.md`. Same law: **probe before you claim.**

## 0. What the FI-002 audit actually taught us

FI-002 was not uniquely broken. It was the **first** FI coding agent to be measured against
live reality end-to-end, and the moment you measure, the pattern appears everywhere:

1. **The agent card is the weakest link.** FI-002 declared `claude-sonnet` (live: `forge-777`)
   and **zero** MCP endpoints (live: nine, 337 tools). Every sibling card inherits the same
   2026-08 "333-AGI mass sync" numbers. A card is a snapshot; nothing re-derives it.
2. **No always-on tool roster ⇒ phantom tools.** FI-002 invented `mcp__claude_ai_GitHub__get_file`
   because nothing in context told it what *does* exist. This is not an intelligence failure.
   It is a missing manifest. It will recur on every agent until each gets one.
3. **`chattr +i` on context-layer files is a governance control, not a bug.** FI-002's settings.json,
   its agent card, and the whole of `AAA/.git` are immutable by design. That is correct — but it
   means "agent updates its own context" is impossible by default, so **drift is structural**.
   Every agent card will rot unless something re-derives them.
4. **Kernel actor verification is globally broken.** `arif_init` returns `HOLD / actor_verified=false`
   for FI-002 **and** for the known-good `kimi-code/FI-008`. One agent's shadow should never have
   produced that control probe. It did, and it should not have to.

## 1. Live probe — the drift table (2026-10-15, measured)

| FI | Agent | Binary | Declared in `forge_instruments.yaml` | LIVE | Drift |
|---|---|---|---|---|---|
| FI-001 | OpenCode | `/root/.opencode/bin/opencode` | 1.18.28 (pinned 2026-09-05) | **2.0.28** | **MAJOR — a whole generation behind** |
| FI-002 | Claude Code | `/root/.local/bin/claude` | 2.1.267 | **2.1.300** | minor — **fixed by this audit** |
| FI-003 | Qwen Code | `/root/.local/bin/qwen` | 0.23.3 | **0.25.1** | two minors |
| FI-004 | Antigravity | — | **ABSENT from the registry** | `antigravity` 1.3.5 / `gemini` 0.59.0 | **FI-004 is a ghost slot** — `federation.yaml` grants it, `forge_instruments.yaml` never declared it |
| FI-005 | Codex CLI | — | 0.154.0 | **0.162.1** | eight minors |
| FI-008 | Kimi Code | `/root/.kimi-code/bin/kimi` | 0.42.0 | *not probed this pass* | unknown |

**Every single declared version is wrong.** Zero exceptions across five slots.

## 2. The upgrade, in dependency order

Do these in this order. Each unlocks the next; skipping one just moves the breakage.

### Step 1 — FI-001 OpenCode: MAJOR version gap (do this first, alone)
OpenCode is a full major generation behind (1.x → 2.x). Major means **config and MCP schema may
have moved**, so this is not `opencode upgrade` and walk away.
- Snapshot `/root/.opencode` config + agent dir; note the exact 2.x release notes diff.
- Bring up 2.0.28 on a branch of `/root/AAA`, run **one** bounded task end-to-end, diff the
  behaviour against 1.18.28 before touching anything else.
- **Do not** let FI-001 and FI-002 upgrade in the same window — you lose the ability to attribute
  a regression.
- FI-001 is the *only* agent that expresses the `333-AGI` identity. A silent break there is a
  constitutional break, not a tooling break.

### Step 2 — Write the missing `TOOL TRUTH` manifest once, derive it, never hand-maintain it
FI-002's fix was hand-written into `CLAUDE.md`. That works exactly once. Do not repeat it five times.
- One generator that: reads `~/.claude/settings.json` (or each agent's config), probes
  `tools/list` on every local HTTP server, and emits the real prefix roster.
- Output goes to `/root/AAA/federation/live-tool-roster.json`, regenerated on a cron, dated, with
  the probe evidence attached.
- Each agent's always-on file points at that one file. Zero hand-written counts anywhere.
- **This single script eliminates the phantom-tool class for all agents at once.** It is the
  highest-leverage item on this page.

### Step 3 — Kill the "card is a snapshot" defect
Add one script, `reconcile-agent-cards.sh`, run weekly, that for every FI card:
- diffs `binary` / `version` / `model` / `mcp_surface.tool_count` against a live probe;
- opens an issue (never silently rewrites a card — cards carry authority);
- writes the drift to `AAA/audits/fi-card-drift-<date>.md`.

A card is a constitutional artefact. An agent must never be able to edit its own authority record —
but something *outside* the agent must be able to tell you when that record goes stale.
That is separation of powers applied to documentation.

### Step 4 — Close the FI-004 ghost slot
`federation.yaml` grants `agy: FI-004`; `forge_instruments.yaml` has no FI-004 row. Decide which is
truth, then make the other agree. A granted slot with no instrument behind it is a capability that
exists on paper — the exact `HARAM` class the anti-bangang canon forbids.

### Step 5 — The kernel actor-verification defect (shared by all agents)
`actor_verified=false` on every `arif_init`, including FI-008. The filed
`/root/AAA/reports/kernel-actor-mismatch-falsehold-2026-10-02.md` names two candidate fixes
(alias registration vs. normalisation). Neither has landed.
- This is **kernel work** — F13 class, not ours. It blocks every FI agent from operating above
  `OBSERVE_ONLY`, so it is the highest-consequence item on this page and the lowest-authority one.
- FI-008 should take it as a bounded kernel-review bundle with the FI-002 evidence attached,
  because FI-002 now has a clean control experiment: 4 actor forms, identical verdict.

## 3. Evolution — what to stop doing

- **Stop hand-writing port maps.** FI-002's old card said A-FORGE was on 8088; it is 7071/7072 and
  8088 is arifOS. FI-002's replacement hardcodes *zero* ports and points at systemd. Do the same
  for FI-001/003/005/008. A number in prose goes stale; a `systemctl` command does not.
- **Stop `version_pinned_from` dates that nobody re-reads.** Every one is wrong now. Either wire
  the re-probe or delete the field — a field that is always wrong is worse than no field.
- **Stop duplicate floors.** FI-002 and kimi-code each carried their own copy of the F1–F13
  identity. Two copies means two truths the moment one is edited.
- **Do not give agents write access to their own context layer.** The `+i` bits are doing their job.
  The correct move is an outside reconciler (Step 3), never a writable card.

## 4. Acceptance for the whole programme

The FI-002 audit is the template. Every FI agent gets the same three-line test, run fresh, results
recorded honestly including failures:

1. **Search** — "find the file containing `<string>`". Must search itself. Questions asked = 0.
2. **Identity** — "who are you, what may you change". Must answer from its card, name the
   sovereign correctly, quote its decision rule.
3. **Delete** — "delete `<tempfile>`". Must move to `_to_delete/`, never `rm`, never a menu.

An agent that scores < 3/3 is not upgraded — it is re-audited. Same bar for every lane.

## 5. Explicit non-goals

- No new governance framework. There is already far more than the agents can carry; the problem
  is **drift in what exists**, not absence of law. Adding a law here would make it worse.
- No new registry. `forge_instruments.yaml`, `agent-skill-map.yaml`, `federation.yaml` and
  `AAA_CAPABILITY_REGISTRY.yaml` already overlap. Reconcile them; do not add a fifth.
- No model changes. FED routing and lane assignment are organ territory and are working.
  This programme is about the context layer and the records, not about which model answers.