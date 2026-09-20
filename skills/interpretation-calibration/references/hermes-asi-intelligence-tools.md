# HERMES ASI Intelligence Tools — MCP enforcement layer

The HERMES RASA MCP server (`/root/HERMES/mcp/hermes-rasa/server.py`, FastMCP, SQLite state at
`/root/.hermes/state/rasa_mcp.sqlite3`, enforcement log at `/var/lib/arifos/rasa_enforcement.jsonl`)
carries five tools that enforce the interpretation-calibration rules at call time.

Call them **before** a reading becomes a claim, a stored record, or an action — not after.

## The five tools

| Tool | Fires on | Enforces |
|---|---|---|
| `hermes_signal_assessment` | Before interpreting | Rule 1 — signal strength caps interpretation width |
| `hermes_motive_boundary` | Before stating anything about a third party | Rule 3 — observable / inference / unsupported split |
| `hermes_calibration_check` | After producing an interpretation | Rule 1 — is the width proportionate to the signal? |
| `hermes_dajjal_check` | Before a consequential action | sensor coverage across affected actors |
| `hermes_calhoun_check` | Before optimising a system | abundance rising while meaning falls |

## Inputs and outputs

- `hermes_signal_assessment(observation, source_reliability, evidence_count, source_type)` →
  `signal_strength`, `max_interpretation_width`, `competing_explanations`, `recommended_action`.
  `evidence_count < 3` or a tertiary/unknown source forces weak + narrow. Always returns at least two
  competing explanations — if more than two survive, the signal is weak.
- `hermes_motive_boundary(statement, actor, evidence_for_motive)` → `observable_facts`,
  `inferences`, `unsupported_claims`, `boundary_violation`, `corrected_statement`. A self-report
  licenses the actor's own state and nothing adjacent; a causal upgrade ("because he wants …") is a
  new claim the report never made.
- `hermes_calibration_check(original_observation, current_interpretation, signal_assessment)` →
  `proportionate` / `over_interpreted` / `under_interpreted` plus what to narrow.
- `hermes_dajjal_check(proposed_action, actors_affected, sensors_present, actors_with_sensors)` →
  `sensor_coverage` (0-1), `vulnerable_actors`, `invisible_consequences`. Below 0.5 = majority of
  affected parties bear the consequence with no voice in the decision.
- `hermes_calhoun_check(system_description, abundance_indicators, meaning_indicators, roles_being_automated)` →
  `calhoun_risk`, `behavioral_sink_signals`, `missing_meaning`, `intervention_points`. Three or more
  roles automated with fewer than two meaning indicators reads critical.

## Why the split exists

The tool set is deliberately **not** a mirror, a clerk, or a witness. Each one takes a reading that
an agent is about to treat as settled and asks whether the evidence carries it. The governing rule
behind all five is one sentence:

> **When signal is weak, interpretation must narrow — not elaborate.**

## Extending the server

- Tools use the `@mcp.tool()` decorator; add new ones after the existing block, never by rewriting
  an existing tool.
- Every new tool should log to the enforcement log via `log_event()` and record its assessment row,
  using content-addressed IDs rather than counters.
- List fields are stored JSON-encoded in SQLite.
- Test through the MCP protocol layer (`mcp.call_tool`), not only by calling the Python function —
  a function that passes while the protocol call fails is not a working tool.
- A gateway process already running picks up new tools only on restart; state plainly that the
  service was patched but not restarted, rather than implying the tools are live.
