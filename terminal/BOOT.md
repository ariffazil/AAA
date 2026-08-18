# Agent boot contract — consume, do not rediscover

> The machine no longer asks agents to figure out reality; it asks agents to operate within a reality already forged by the institution.

```
LAW            ← /root/arifOS/GENESIS/000_KERNEL_CANON.md   (floors / constitution)
               ← /root/AAA/prompts/INIT.md                 (federation bootstrap)
STATE          ← /root/AAA/terminal/state.json
HANDOVER       ← /root/AAA/telemetry/handover.log
FLOW           ← arifFLOW :7073  (metabolize only — not a 7th ledger)
CAPABILITIES   ← /root/AAA/registries/models/CAPABILITIES.json
MODELS         ← /root/.config/federation-models.json
TASK
```

TOOLS.json and SKILLS.json are not minted. Do not invent them.
Until they exist: existing `SKILL.md` files are recipes; MCP/API surfaces are hands. Model is chosen last.

## Clerk, not archaeologist

On spawn, run:

```bash
/root/AAA/terminal/boot.sh
```

That is enough to know authority, mode, FQ, mission, law, WELL.

Do **not** at init:

- `curl :7073` to infer FQ
- `curl :8088` to infer thermo SEAL / mission / holds
- `curl :18083` to infer operator fatigue
- scan MOTD, PS1, hero, FED, and cache and pick a story

Hero already thought. You read `state.json`.

## Bind is not archaeology

`arif_init` still binds identity (session_id / SCT). That is law, not a second FQ computer.

`now` is the deep probe. Call it when you need time, FRAME, vault counts, or carry — not to learn FQ.

## Gate from the board

| Board says | You do |
|---|---|
| `mode=HOLD` | Governance-first. No extra verification loops. **Not a deny-boot.** Harnesses still wake. |
| `fq_state=FOSSILIZED` | Execute SEALed work. Stop outcome-neutral checks. |
| `well=HOLD` | Sensor debt, not "Arif is tired." |
| `state.json` missing / STALE | Run `hero --observe`. Do not curl organs yourself. |

## FQ heuristic (now — kill the V loop)

Board `FOSSILIZED` (V ≫ X) means:

- Do the SEALed task. Increment **X**.
- Do not open a discovery/research loop unless 888 asked for one.
- If a check cannot change the decision, skip it.
- Do not re-probe organs, mcp.json, or keys. Trust `state.json` + CAPABILITIES.

Institution verifies **between** boots (audit, SOT). Clerk is an X engine.

**Not minted yet (do not pretend):** OS does not auto-mount `voice_design` from a capability request. That is Phase 6 after TOOLS.json. Today: use existing `SKILL.md` / already-wired MCP. Do not invent a handshake.

## Drift test

If two agents disagree on FQ, one of them probed. Only hero writes `state.json`.

## Institutional RSI — Option B only

Clerks execute. They do not rewrite ledgers.

- **A** (manual mint) — allowed, slow.
- **B** (proposal clerk → PR → F13 merge) — the zen path. Machine suggests. 888 turns the key.
- **C** (autonomous SOT mutation) — VOID. Illegal operation.

A clerk that hits an edge case fails loudly. It does not invent a workaround and does not edit `CAPABILITIES.json`, `state.json`, or future TOOLS/SKILLS.

## Out-breath / In-breath (ephemeral ↔ eternal)

Clerks do not learn. The institution changes physics between boots.

```
888 INTENT
    → bind LAW + STATE
    → SKILL (not minted — use existing SKILL.md recipes)
    → TOOL  (not minted — runtime MCP / API only)
    → CAPABILITIES
    → MODEL last
    → execute
    → write exhaust (fail loudly; do not rewrite SOT)
         │
         ▼
    Proposal clerk reads exhaust → PR only
         │
         ▼
    F13 merges → next boot is structurally smarter
```

Identity is jurisdiction, not personality. Memory that survives death is telemetry + sealed SOT, not a chat window.

Deny-boot only: `kernel=down` / GHOST, F13 VOID, or board missing after `hero --observe` fails.
