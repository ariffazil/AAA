---
name: agent-session-forensics
description: "Use when asked how a prior run produced something."
version: 1.0.0
tags: [forensics, state-db, provenance, session-audit, subagent-dispatch, artifact-hash]
---

# Agent Session Forensics

Class-level skill. Trigger: "how were you able to generate this?", "what prompt did I give you?", "did that run really use subagents?", "which skills/tools were used?", or any moment a claim about process (yours or a peer agent's) needs checking against the record.

## The one rule

The chat transcript is testimony; the ledger is evidence. Answer process questions from the runtime store and the artifact hashes on disk, never from memory of the conversation.

Corollary: **never claim an orchestration layer the ledger does not contain.** Many impressive-looking deliverables are one linear loop with a lot of tool calls, and reporting "0 subagents, N tool calls, one session" is a complete, correct, and more trustworthy answer than an inferred multi-agent pipeline. Only describe agents or a swarm when `delegate_task` entries or `async_delegations` rows exist.

## Ledger map

Primary store: `/root/.hermes/state.db` (SQLite). Probe the schema before querying — column names are not the intuitive guesses.

| Table | Carries |
|---|---|
| `sessions` | id, source, chat_id, chat_type, display_name, model, model_config, system_prompt_hash, started_at/ended_at, message_count, tool_call_count, title, tool_names, profile_name |
| `messages` | id, session_id, role, content, **tool_calls** (JSON array of `{function: {name, arguments}}`), tool_name, timestamp, token_count |
| `system_prompts` | hash -> the fully assembled system prompt for any session |
| `async_delegations` | delegation_id, state, dispatched_at, task_json, result_json — the subagent ledger |

Secondary stores: `~/.hermes/logs/gateway.log` and `agent.log` (chronology and delivery; multi-GB, grep never read), `~/.hermes/sessions/sessions.json`, `/root/.local/share/arifos/forge_receipts/*.json` (artifact provenance), and the artifact directory's `SHA256SUMS.txt`.

Note: `~/.hermes/.hermes_history` is a *different* store from `state.db`. A grep there returning nothing proves nothing — the full record lives in the ledger.

## Procedure

1. **Locate the sessions.** `select distinct session_id from messages where content like '%<entity>%'`, then read the matching `sessions` rows for model, chat, title, counts, window.
2. **Recover the asks verbatim.** `select id, role, timestamp, substr(content,1,600) from messages where session_id=? and role='user' order by id`. Quote these exactly; never paraphrase what the principal asked.
3. **Rebuild the tool histogram.** Walk the rows, `json.loads` each `tool_calls`, count `function.name` (and read `arguments` for the interesting ones). This is the answer to "what tools were used", with counts.
4. **Recover the skills actually loaded.** Filter those same entries for `skill_view` and read `.name` out of the parsed arguments — the loaded set, not the available set.
5. **Check subagent dispatch.** Any `delegate_task` calls, plus `select * from async_delegations where origin_session_id=?`. Zero is a finding, not an omission.
6. **Identify the exact system prompt.** `sessions.system_prompt_hash` -> `system_prompts.prompt`. Report its length and its section structure (regex the headings) rather than dumping it.
7. **Grade the artifact.** `sha256sum` the returned or delivered file against the `forge_work/` copy, its `SHA256SUMS.txt`, and the forge receipt. Identical hashes close the loop: what was produced is what came back, so any remaining disagreement is about content, not corruption.

## Episode reconstruction — "find the earlier thread and map the reality"

A different question from "how was this artifact produced": the principal points at the TAIL of a long external thread (an email, a dispute, an outsider's request) and wants the whole chain back plus where it stands now. Answer in three layers, in this order.

1. **Chain of custody — what was already said, promised, or sent.** Query `messages` by TIME WINDOW around the known anchor (the date on the tail document), not by guessed keywords alone:

   ```sql
   select id, datetime(timestamp,'unixepoch'), role,
          substr(replace(content,char(10),' | '),1,600)
   from messages
   where timestamp between strftime('%s','<anchor - 2h>') and strftime('%s','<anchor + days>')
   order by id limit 200;
   ```

   Then keyword-sweep the whole estate for the counterparty's name(s), the subject line, and the artifact filenames. The rows that matter are the ones recording an OUTWARD action: `role='tool'` entries carrying an API response with a `messageId`/status, and `assistant` rows stating what was sent. **Commitments live in the transcript, not in the tool's own store** — an outbound email lane has no queryable sent-items ledger here, so the transcript row IS the receipt.

2. **Verify the claims those old sessions made, against the live surface.** A prior session's "fixed and deployed" / "sent" / "signed" is testimony. Re-check each one now: `git log --oneline -1 <sha>` for every commit it cited, `md5sum` the DEPLOYED copy against the source repo, `grep -c` the call sites of the fix, `curl` the health and public endpoints, query the remote API for any registry entry claimed. Report each as CONFIRMED / STALE / ABSENT instead of repeating the old narrative — a chain reconstructed from the transcript alone will carry a dead claim forward.

3. **State the open decisions, not a recommendation dump.** The reconstruction's value is showing which threads are already closed and which are still waiting on a human. End there.

Sweep the off-ledger stores for pre-compaction artifacts too: quarantine trees (`/root/.quarantine/**` keeps dated `_quarantine/<YYYY-MM-DD>/` directories holding the original drafts and the failed-run logs), `~/.hermes/pastes/`, `~/.hermes/cache/documents/`. A draft found there tells you what was INTENDED; compare it against the transcript before quoting it as what was sent.

## Pitfalls

- **A draft on disk is not a sent message.** Quarantine copies exist precisely because the send lane failed. Only an API response row (messageId/status) in the transcript proves delivery. Never report "we replied" from a draft file.
- **Scope broad greps or they time out.** `grep -ril <term> /root` over this estate (multi-GB quarantine, dozens of venvs, vendored tool trees) blows a foreground timeout. Restrict to the likely trees and exclude `node_modules` / `.venv` / `backups` / vendored CLI dirs — or run it backgrounded with `notify`.
- **Prior-session artifacts may no longer exist where they were written.** Attachments and generated media are not persisted by the lanes that send them; if a delivered artifact must survive a later audit or re-send, it has to be re-written to a stable repo path, or regenerated from its source. Say which of those you can do rather than promising the file back.
- **`PRAGMA table_info(<table>)` first.** The time column is `timestamp`, not `created_at`; guessing fails the query before it runs.
- **Timestamps are epoch floats.** Convert before reporting, and state the window you actually covered.
- **Never print whole rows from `messages` or `system_prompts`.** Prompts run 30–100 KB and there are hundreds of them. Print lengths, hashes and matched markers; always `substr(content, 1, N)` in the query.
- **Sweep every session, not just the current one.** Several agent sessions can be live and mutating mid-investigation. A partial window is not the world: check all sessions before attributing an action, and say which window you checked.
- **Report counts, not adjectives.** "57 tool calls, 0 subagents, 3 skills loaded, 2 artifacts" is auditable; "a heavy agentic pipeline" is not.
- **When the review finds your own error, lead with it.** A forensic answer is also a falsifier of your own prior output — a corrected figure with the mechanism attached is worth more than a clean-sounding summary.
- **Repetition discipline still applies.** Reading a ledger is not a licence to repeat private content outward.

## Verification checklist

- [ ] Session id(s) and time window stated
- [ ] Tool counts derived from parsed `tool_calls`, not from recollection
- [ ] Subagent count checked in both `tool_calls` and `async_delegations`
- [ ] The principal's prompts quoted verbatim from `messages`
- [ ] Returned artifact hash compared to `SHA256SUMS.txt` before commenting on it
- [ ] For multi-session threads: each prior session's outward claims (sent / fixed / deployed / signed) re-probed live, not restated
- [ ] Any claim about the run the ledger cannot support explicitly marked UNVERIFIED

*DITEMPA BUKAN DIBERI*
