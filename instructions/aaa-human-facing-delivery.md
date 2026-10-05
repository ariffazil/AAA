# AAA Human-Facing Delivery — Standing Rule

> **Status:** DRAFT_AWAITING_F13 (2026-10-06 · mission AUTH_RUNTIME_REALITY_001)
> **Sovereign chat:** `267378578` (Telegram DM, F13)
> **Canonical:** this file. Patch `/root/.hermes/config.yaml::aaa_human_facing_routing` per Appendix A.

## What this rule covers

Any artifact produced by an AAA agent whose **primary consumer is Arif**
must be delivered to the sovereign Telegram on completion, not just
written to the repo.

## Human-facing artifact kinds (route to Telegram)

- `doctrine_md` — new/changed constitutional or operational doctrine
- `audit_report` — F1-F13 floor audit, drift report, falsification round
- `sovereign_brief` — daily/weekly brief, sovereign-pulse output
- `decision_request` — anything that asks Arif to binary-yes/no a path
- `f13_binary_prompt` — constitutional mutation awaiting F13 sign-off
- `agent_alignment_change` — AGENTS.md diffs affecting citizen role/boundary
- `new_artifact_in_repo` — first creation of a file in /root/AAA or /root/.hermes that
  carries an audience-of-one implication (drafts, schemas, infra-policy do not)

## Internal artifact kinds (do NOT route)

- `schema_json` — machine contract
- `test_fixture` — eval inputs
- `code_change` — implementation, even large
- `receipt_jsonl` — provenance, lives in git
- `log_file` — telemetry, lives in journal
- `in_band_hash` — seal/signature material

## How the rule is enforced

Two layers:

1. **Agent self-check** — before declaring a task COMPLETED, the agent
   asks: "is this artifact human-facing per the kinds list?" If yes,
   fire `hermes send --to telegram:267378578 <summary>` with:
   - artifact path
   - 1-line summary
   - delivery timestamp
   - sha256 of artifact

2. **Hook** (when wired) — `arifos-human-facing-route-hook.py` reads
   recent file-creation events in /root/AAA and /root/.hermes, classifies
   per the kinds list, and emits a routing receipt. Fail-closed.

## Appendix A — config patch (Arif to apply)

Append to `/root/.hermes/config.yaml` under the `cron:` block:

```yaml
# F13 2026-10-06 (Arif directive): human-facing AAA artifacts auto-route
# to sovereign Telegram 267378578. Provenance stays in git; this is
# notification, not publication.
aaa_human_facing_routing:
  sovereign_chat: '267378578'
  transport: telegram
  applies_to: [AAA_organs, citizen_agents]
  kinds_routed: [doctrine_md, audit_report, sovereign_brief, decision_request,
                 f13_binary_prompt, agent_alignment_change, new_artifact_in_repo]
  kinds_NOT_routed: [schema_json, test_fixture, code_change, receipt_jsonl,
                     log_file, in_band_hash]
  delivery_template: 'hermes send --to telegram:267378578 "<path> | <1-line summary> | sha256:<hash>"'
```

Or via `hermes config` once that command exposes nested keys.

## Why this exists

Arif has been burned by agents that "completed" work that he never saw
because the artifact lived in a repo he wasn't watching. This rule
guarantees: any artifact whose primary consumer is Arif reaches his phone
within the same session boundary. The git record remains the truth;
Telegram is the reminder.

REALITY > EVERYTHING.
