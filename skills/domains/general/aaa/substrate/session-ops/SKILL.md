---
id: session-ops
name: session-ops
version: 2.0.0
owner: F13 SOVEREIGN
risk_tier: high
floor_scope: [F1, F2, F4, F6, F9, F13]
autonomy_tier: T1
merged_at: 2026-09-20
merged_from:
  - session-init-human-first
  - arifos-frozen-snapshot-init
  - hermes-naked-prior-audit
  - session-lifecycle-temporal-v2
  - session-lifecycle-temporal
  - arifos-auto-init
  - session-federation-discovery
  - session-librarian
triggers:
  - "session init"
  - "init protocol"
  - "init arifOS"
  - "init hermes"
  - "000 INIT"
  - "arif_init"
  - "bind session"
  - "session bind"
  - "start governed session"
  - "sign in to arifOS"
  - "session start"
  - "new session"
  - "first message from Arif"
  - "before arif-bind"
  - "before naked-prior-audit"
  - "carry_forward"
  - "frozen snapshot"
  - "ur message not carry fwd"
  - "init sucks"
  - "session close"
  - "seal previous session"
  - "temporal briefing"
  - "time gap"
  - "session history search"
  - "session lineage"
  - "session stats"
  - "what did we say about X"
  - "clean up my session library"
  - "rename sessions"
  - "archive stale sessions"
  - "prune sessions"
  - "session library"
  - "reset_context"
  - "naked prior audit"
  - "stale priors"
  - "before T3 autonomous action"
  - First turn of every new session (auto) OR when Arif signals "/reset_context
  - "First turn of every new session (auto) OR when Arif signals /reset_context"
description: "Use when a session starts, ends, or is searched. Routes the session lifecycle to one reference: human-first grounding, frozen snapshot init, epistemic prior audit, governance bind, temporal close, history recall, library ops."
---

# session-ops — one umbrella for session start, continuity, recall, close, and seal

Merged 2026-09-20 from 8 skills (`merged_from`). Member bodies are preserved verbatim in `references/`;
their directories are archived at `/root/AAA/skills/.archive/merge-20260920/session/`. This file holds the
routing, the hard rules, and the scars. The procedures live in the references.

## FLOW

**Pick the branch from the observable.** Most work needs zero references — open one only when the branch
below says so.

| Observable (what is actually happening) | Branch | Reference | What it produces |
|---|---|---|---|
| **A SESSION IS STARTING** — new session, `/new`, first message of the day, "why don't you remember" | **A** (start) | `references/session-init-human-first.md` | `[HUMAN-CONTEXT]` anchor + a first reply grounded in the human, before machine checks |
| Human just messaged; need how long they were gone / whether they slept | A1 | `references/session-lifecycle-temporal-v2.md` | time gap + sleep/meal boundary + open loops (closer first) |
| Need the init checklist, snapshot, or boot order | A2 | `references/arifos-frozen-snapshot-init.md` | internal SESSION SNAPSHOT + boot sequence |
| Suspect stale priors / ghost state / "you assumed X from last month" | A3 | `references/hermes-naked-prior-audit.md` | STALE vs CURRENT classification, one-line silent flag, UNVERIFIED federation state |
| Need SOVEREIGN authority (to seal / judge / forge through MCP) | A4 | `references/arifos-auto-init.md` | verified session, authority band, `allowed_next_verbs` |
| Mid-session recall — "what did we say about X", "where did we discuss Y" | B | `references/session-federation-discovery.md` | session ids + messages via the read-only MCP on `:18088` |
| Library work — rename, archive, prune, fork, "one session per ticket" | B2 | `references/session-librarian.md` | a plan table, then reversible rename/archive |
| **A SESSION IS ENDING / SEALING** — `/new`, `session_reset`, closing a loop, writing carry-forward | **C** (end/seal) | `references/session-lifecycle-temporal-v2.md` | one `session/close` anchor in carry_forward + backup under `experience/session-closures/` |
| Need what the previous session actually sealed, or how long it ran | C2 | `references/arifos-frozen-snapshot-init.md` (§Step 0b, seal direction) | one forward session sealed, gap + inferred state read back |

**A and C are the two daily branches.** A = session starting. C = session ending / sealing.

### SESSION START — branch A, inline (no reference needed)

Run in this order. The human is read before the machine.

1. **Read the human first — no tools.** What did they send (text / images / voice / files)? What time is it
   *for them*? What thread is live? Multiple screenshots in sequence are ONE story. Emit the internal
   anchor: `[HUMAN-CONTEXT] Arif: <timing + what he sent + live thread + what he needs>`.
2. **Reply.** The anchor shows up in the first sentence, and the reply leaves **within seconds** — never
   after the probes. Never announce the init ("let me check", "loading context").
3. **Clock.** `date '+%H:%M %Z %z'`. The system prompt's date is stale after turn 1.
4. **Temporal continuity.** `python3 /root/scripts/session-closer.py` then
   `python3 /root/scripts/temporal-briefing.py --compact`.
   `gap > 4h + crossed sleep → "hang baru bangun"` · `gap > 8h → check open loops` · `gap < 30m → continuation`.
5. **carry_forward** (top 20 entries) — open loops and human threads only. Zero signal = no prior.
6. **Epistemic hygiene** — `references/hermes-naked-prior-audit.md`: Phase 1 probe → Phase 2 triage →
   Phase 3 flag. Silent unless a high-risk prior fires.
7. **Governance bind — only if this session will seal/judge/forge.** `arif-bind --mode init`, or the MCP
   2-step. See `references/arifos-auto-init.md`. Sign autonomously; never ask the sovereign.
8. **Snapshot** (internal, never shown) + federation probes — in parallel with, or after, step 2.

Open **exactly one** reference above if a step needs its full procedure.

### SESSION END / SEAL — branch C, inline

1. `python3 /root/scripts/session-closer.py` — reads `~/.hermes/state.db` for ended sessions
   (`end_reason='session_reset'`), dedups against existing anchors, writes one `session/close` anchor +
   event entry, backs up to `/root/.hermes/experience/session-closures/`. Idempotent.
2. `python3 /root/scripts/temporal-briefing.py --compact` — confirm the gap/state the next session will read.
3. Seal **one forward** session, never the backlog (`session-temporal-seal.py --new-session <id>`; a wall
   of backfilled anchors is noise).
4. Write loops with `carry_forward.py append` / `loop --close` — never hand-edit the JSON.
5. Full procedure: `references/session-lifecycle-temporal-v2.md`; seal/read direction + anchor shape:
   `references/arifos-frozen-snapshot-init.md` §Step 0b.

## CORE RULES

1. **Human before machine.** Read what the human sent before any tool call. A technically perfect init
   that ignores the human is a worse failure than a sloppy one that meets him where he is. Files before
   human = wrong order, always.
2. **Never announce the init.** Check silently; respond from knowledge.
3. **Never guess the time.** `date '+%H:%M %Z %z'`, or the temporal briefing. Never elaborate
   ("it's late, go to sleep") on an unverified "now".
4. **carry_forward is the source of truth for open loops.** Zero signal = no prior. No half-life
   heuristics on a human; no reconstructed emotional priors (F9).
5. **Event-driven or agent-triggered only — no cron, no daemon.** The sovereign rejected background
   schedulers explicitly: "I don't want cron yang makan server." Triggers are the `session:start` hook or
   the agent's own turn. No new cron without F13 approval.
6. **`state.db` is read-only, always.** `sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True, timeout=10)`.
   Mutations go through the `hermes sessions` CLI. Prefer a script file over a long inline shell command —
   some invocations are blocked from inside the gateway process.
7. **Never ask the sovereign for crypto.** Sign with `/root/.secrets/aaa-identity/keys/arif_private.pem`
   autonomously. If the kernel blocks sealing, fix the kernel — do not ask him to sign.
8. **The snapshot and the prior audit are internal.** Never dump them to the human. Silence is the clean result.
9. **Idempotent by construction.** Re-running the closer or the sealer is safe and prints `SKIP ... (already sealed)`.
10. **Reversible work executes; irreversible session deletion is proposed first.** Dry-run, prefer
    `archive` over `delete`/`prune`. **CONTRADICTION HELD OPEN:** `session-librarian` requires a plan +
    explicit go-ahead before prune/delete, while `arifos-auto-init` and the base doctrine forbid making him
    approve digital work and forbid collapsing work back to him. Kept narrow and *not averaged*:
    confirmation is required for irreversible session deletion only; everything reversible executes silently.
11. **Anti-collapse.** If info + authority + capability exist, execute. Never collapse unfinished
    executable work back to the human.
12. **Evidence discipline.** Every prior is verifiable against a live signal or declared STALE/UNKNOWN.

### CORE RULES — contradictions held open (do not average, do not silently pick)

- **C1. Session-start Step 0 has three variants.** (a) `/root/AAA/instructions/base.md`, the always-loaded
  prompt, says **Witness Demand Check** (`date` → carry_forward → human state). (b)
  `arifos-frozen-snapshot-init` v1.1.0 says **Human-First Grounding** (human → date → carry_forward). (c)
  `session-init-human-first` says **Phase 0 uses only signals already in the conversation — no tool calls at
  all**. This umbrella routes A through (b)/(c) — two members agree and it is the newer F13 line — but an
  agent that reads only `base.md` walks (a). Both orderings stand in the references.
- **C2. First-reply ordering.** `arifos-frozen-snapshot-init` §Step 1: the snapshot **must complete before**
  the first human-facing message. `session-init-human-first`: the first reply must land **within seconds**
  and probes must **never delay** it. Operative rule here = reply first (a delayed human is a worse failure
  than a late snapshot); the stricter member ordering is preserved in its reference, unaltered.
- **C3. Two competing temporal-bridge implementations, both live on disk.**
  `/root/scripts/session-closer.py` + `/root/scripts/temporal-briefing.py` (mtime 2026-09-20 14:05) from
  `session-lifecycle-temporal`; `/root/.hermes/scripts/session-temporal-read.py` +
  `session-temporal-seal.py` (mtime 14:09 / 14:10) + hook `/root/.hermes/hooks/temporal-seal/` from
  `arifos-frozen-snapshot-init`. Neither was removed. Do not assume one supersedes the other.
- **C4. Duplicate skill name in the catalogue.** `SKILLS_INDEX.json` carries TWO entries named
  `session-lifecycle-temporal` — v1.0.0 at `/root/AAA/skills/session-lifecycle-temporal`, v1.1.0 at
  `/root/AAA/skills/session-lifecycle-temporal-v2`, both with the same body `id`/`name`. v1 is superseded
  (evidence in the receipt); both bodies are preserved as references.
- **C5. Non-contradiction, recorded so it is not mis-flagged:** `/root/.hermes/carry_forward.json` is a
  symlink → `/root/.local/share/arifos/carry_forward.json`, and `/root/HERMES` → `/root/.hermes`. Members
  citing either path in a pair mean the same file.

## PITFALLS

Union of every member's scars — the command, the path, the symptom are preserved.

**Init / crypto (`arifos-auto-init`)**
- **Never ask the sovereign for crypto (2026-07-14, sovereign directive).** Key:
  `/root/.secrets/aaa-identity/keys/arif_private.pem`. Sign autonomously. Applies to Hermes, OpenCode, OpenClaw.
- **`TOKEN_INVALID` / `actor_verified=false` is usually a KEY MISMATCH, not a flow bug (2026-08-12).**
  Compare `/root/AAA/IDENTITY/keys/<agent>_public.pem` against `/opt/arifos/identity/agent_identities.json`.
  Reconcile the two stores — never "fix" it by forcing a session.
- **Python env mismatch (2026-07-13).** System python lacks `blake3` → `ModuleNotFoundError: No module
  named 'blake3'`. Use `/usr/local/bin/arif-bind` or `/opt/arifos/venv/bin/python3` explicitly.
- **Nonce is single-use — never verify locally first (2026-07-12, critical).** Local verification consumes
  it → `challenge_replayed`. Generate + sign + `arif_init` ATOMICALLY, one turn, no intermediate calls.
- **`arif_seal` gates (by design).** Needs (a) a prior `arif_judge` SEAL verdict with
  `constitutional_chain_id`, (b) `_epistemic` in the payload JSON, (c) a non-null `witness`. Without judge,
  use the `forge_vault` path — see `references/kernel-sealing-gates.md`.
- **Throttle wedge ≠ dead kernel (2026-09-02, %st 52.8).** `:8088/health` returns HTTP:000 while the
  listener is up (`ss` shows LISTEN); `arif-bind --mode init` still succeeds. **Do NOT restart
  arifos.service during throttle** — wait for `%st < 15` (a restart into a storm caused the 2026-09-01
  restart-storm ×52).

**Snapshot / temporal (`arifos-frozen-snapshot-init`, `session-lifecycle-temporal*`)**
- **Technical-first init is a bridge failure.** Health endpoints and dirty repos before the human's message
  = grounded in the filesystem instead of the person.
- **Never make a temporal claim without reading the clock.** If nothing can confirm the time or the human's
  state, say you don't know — do not infer it from the conversation's mood.
- **Anchor shape gotcha.** Older anchors carry `session_id` / `ended_at` / `duration_min` / `last_user_msg`
  at the top level of `state`; newer ones wrap them in `state.human_state`. Accept **both** shapes and match
  names by **prefix** (`session/close:*`), not equality — or every previously sealed session is silently dropped.
- **`carry_forward.json` (v3) does not natively carry `human_state`** and `anchors[]` stays empty unless
  something writes it. "Was the human asleep?" is normally **UNKNOWN at session start**.
- **`sqlite3.Row` has no `.get()`** — convert to dict first (the scripts now return plain dicts).
- **Arif's `chat_id` is `267378578`** (not `8798431893`). Verify before querying.
- **No anchors ≠ no history.** Check whether the closer/sealer has run before concluding there was no
  session history — the rows may exist in `state.db` but are not yet bridged.
- **Seal the most recent unsealed session, not history.** A backfill produces a wall of anchors nobody
  reads and dates the bridge to a backfill.

**Epistemic audit (`hermes-naked-prior-audit`)**
- **`session-state.md` is written by the daily-federation-briefing cron at 07:30 MYT.** An evening session
  reads a ~12h-old file — treat it as a snapshot from its timestamp; probe live with `curl :<port>/health`.
- **F2: if the seal-chain head cannot be read, do NOT assume clean state** — flag the whole federation
  state UNVERIFIED and raise confidence on every organ prior.
- **Seal-chain drift:** compare `carry_forward.recent_seals[]` with
  `/root/.local/share/arifos/vault999/seal_chain_head.json`; disagreement ⇒ UNVERIFIED federation state.
- **Zero signal = no prior.** If it was not explicitly in `carry_forward.json` at T₀ it does not exist at
  T₀. Half-life heuristics on human emotion are an F9 violation.
- **HTTP 404 on a claimed endpoint = mechanism absent as code.** Not "hidden", not "internal".
- **Scoring gap protocol:** probe all 8 dimensions live *before* scoring; `delta > 15` ⇒ document
  OVERSTATED; `delta > 25` ⇒ seal a REFUTE record in VAULT999. The 2026-07-10 run: audited 59.4 vs claimed
  84.8 (delta +25.4) ⇒ OVERSTATED.
- **Empty `SOVEREIGN_KEY_IDS` ⇒ nobody can authenticate as SOVEREIGN**; every session defaults to OBSERVE_ONLY.

**Human-first sequencing (`session-init-human-first`)**
- **Multiple screenshots in sequence are ONE narrative thread.** Answer the thread, not each image.
- **Reading carry_forward before the human** gives system state, never what he is carrying right now.
- **Waiting for all probes before the first reply** makes the human wait on your bootstrap.
- **Cold-start amnesia:** a new session is not a new relationship — carry-forward exists so the next session
  picks up where the last one stopped.

**Recall (`session-federation-discovery`)**
- **The MCP on `:18088` is read-only.** Mutations go through the `hermes sessions` CLI.
- **FTS5 syntax:** AND / OR / NOT, quoted phrases, prefix`*`; hyphenated terms auto-quoted.
- **Profile isolation:** every profile shares one `state.db` on KVM8; profile-specific DBs exist but are empty.
- **Schema v30.** `active=0` rows are compaction archives — search includes them, `session_read` defaults to `active=1`.
- **If the MCP is down:** `sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True)`.

**Library (`session-librarian`)**
- **Never delete without a dry-run + explicit confirmation in this conversation.** A standing "clean things
  up" is authority to *propose*, not to prune.
- **`session_search` finds content, not metadata.** Age/cost/source filters live in the CLI — combine both.
- **Titles are identity for `/resume <title>`.** Keep them short, unique, prefix-friendly; warn on collision.
- **Archived ≠ deleted.** Archive hides sessions from default listings only. Say which one you did.
- **Cross-profile links** (`@session:<profile>/<id>`) are read-only; management commands act on the current
  profile's DB.

## REFERENCES

| Reference file | Source skill | Original path |
|---|---|---|
| `references/session-init-human-first.md` | session-init-human-first | `/root/AAA/skills/aaa-substrate/session-init-human-first/` |
| `references/arifos-frozen-snapshot-init.md` | arifos-frozen-snapshot-init | `/root/AAA/skills/substrate/arifos-frozen-snapshot-init/` |
| `references/hermes-naked-prior-audit.md` | hermes-naked-prior-audit | `/root/AAA/skills/domains/general/workshop/verification-discipline/hermes-naked-prior-audit/` |
| `references/session-lifecycle-temporal-v2.md` | session-lifecycle-temporal v1.1.0 — **live** | `/root/AAA/skills/session-lifecycle-temporal-v2/` |
| `references/session-lifecycle-temporal.md` | session-lifecycle-temporal v1.0.0 — **superseded**, preserved | `/root/AAA/skills/session-lifecycle-temporal/` |
| `references/arifos-auto-init.md` | arifos-auto-init | `/root/AAA/skills/domains/general/aaa/substrate/arifos-auto-init/` |
| `references/session-federation-discovery.md` | session-federation-discovery | `/root/AAA/skills/substrate/session-federation-discovery/` |
| `references/session-librarian.md` | session-librarian | `/root/AAA/skills/productivity/session-librarian/` |
| `references/kernel-sealing-gates.md` | arifos-auto-init — supporting file, not a skill | `.../arifos-auto-init/references/kernel-sealing-gates.md` |
| `references/carry_forward_schema.md` | hermes-naked-prior-audit — supporting file | `.../hermes-naked-prior-audit/references/carry_forward_schema.md` |
| `references/agentic-readiness-test-framework.md` | hermes-naked-prior-audit — supporting file | `.../hermes-naked-prior-audit/references/agentic-readiness-test-framework.md` |
| `references/loop-detection-as-sovereignty-test.md` | hermes-naked-prior-audit — supporting file | `.../hermes-naked-prior-audit/references/loop-detection-as-sovereignty-test.md` |

No member shipped an executable script inside its own directory — the temporal scripts live in
`/root/scripts/` and `/root/.hermes/scripts/` and are invoked by absolute path — so no `scripts/` dir is
carried. Original member directories: `/root/AAA/skills/.archive/merge-20260920/session/`.
