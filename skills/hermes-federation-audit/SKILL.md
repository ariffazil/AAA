---
name: hermes-federation-audit
description: "Use on /000 INIT Hermes federation audits (A-I sections)."
owner: arifOS
capability_tier: fed-long-context
ecology_state: WARM
---

# Hermes Federation Audit (the /000 INIT class)

> Produce a section-A-through-I structured audit of the active Hermes prompt scaffold, context-assembly path, gates, and federation flow. Read-only. No mutation, no secret export, no narrative padding.

## When this fires

A sovereign-directed `/000 INIT` request, or any equivalent prompt that asks for:

- A bracket map of instruction layers (00 bootstrap → 99 audit wrapper)
- A precedence / conflict matrix across those layers
- An end-to-end federation flow map for a read-only probe request
- A gate-enforcement test battery (F13, write-gate, prompt-injection, secret, delegation, audit, MCP state, fallback)
- An MCP inventory table with declared-vs-observed states
- A machine-readable receipt + a one-paragraph "honest gate map"

If the request only asks for ONE gate audit (e.g. "is the mail gateway enforced?"), use `chokepoint-enforcement-audit` instead — that is the narrower skill.

## Reality-first probe order (do not reorder)

The audit's authority depends on having probed the live state before reading config. Run probes in this order:

1. **Runtime identity** — `hermes --version` (binary path, upstream commit, local commit, install method, Python). `id`, `hostname`, `date`.
2. **Process tree** — `ps -eo pid,ppid,etime,user,cmd | grep -iE "hermes|1mcp|gateway|aforge"` filtered to the actual federation processes. The PID list is the witness for "is this thing actually up."
3. **Service states** — `systemctl list-units --type=service --state=running --no-pager --no-legend | awk '{print $1}' | sort`. The list itself is the audit evidence — not a doc.
4. **Prompt-scaffold files (existence + ownership, not content)** — `stat` on `/root/AGENTS.md`, `/root/CLAUDE.md`, `/root/.hermes/SOUL.md`, `/root/.hermes/AGENTS.md`, `/root/.hermes/config.yaml`, and the active profile's `config.yaml`. Then `sha256sum` on the same. Provenance hashes anchor the bracket map.
5. **MCP health** — read `/root/.hermes/MCP_HEALTH.json`. Status vocabulary is fixed: `healthy | ready | degraded | down | unavailable | disabled-intentional | unauthorized | expired | unknown`. Do not invent status words; do not collapse `stdio_present` into `healthy`.
6. **Critical-port probes** — `</dev/tcp/127.0.0.1/<port>` for each federation port (8088 arifOS, 7073 arifflow, 7071 A-FORGE, 8791 claim-ledger, 18083 WELL, 18085 FRAME, 4000 FED). OPEN vs closed is binary evidence; don't curl unless you want JSON.
7. **Live kernel health** — `curl -s --max-time 3 http://127.0.0.1:8088/health` for the canonical federation health payload. This carries floors_active, vault_sealer_breaker, runtime_drift, contract_drift, surface_consistency.
8. **Gate hooks** — for each "this is the gate" claim, find the actual file wired into `hooks.pre_tool_call` of the active profile. The deprecated skeletons (`/root/.hermes/gate/hermes_mutation_gate.py`, `mutation_gate_hook.py`) are NOT the live gate — they say so in their own headers. The live gate in this federation is `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py`. Verify in the profile config, not by import-graph.
9. **JITU (the circuit breaker)** — `/root/AAA/federation/kernel/jitu.py`. Single authority. `check` is the live enforcement call. Fail-closed on any fault.
10. **Hook receipt trail** — tail `/root/.local/share/arifos/hermes_hook_receipts.jsonl`. The K-02 transition (`k02_transition: true`) is the receipt that a pre_tool_call hook actually fired.
11. **Constitutional source files** — `/root/AAA/canon/APEX-REALITY-KERNEL.md`, `/root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md`, `/root/AAA/instructions/authority-envelope.md`, `/root/AAA/instructions/state-transition-discipline.md`. These are CONFIG-DERIVED, not PROBED, until a sealed runtime check confirms them.
12. **Carry-forward + memory state** — read `/root/.hermes/carry_forward.json` (symlink target: `/root/.local/share/arifos/carry_forward.json`) for open loops, human state field. Do not write.

Stop probing after 12. Anything past that is decoration, not evidence.

## Bracket map sections — the 10 layers that actually matter

Use these labels verbatim — they map to the spec template and to the constitution:

```
[00 BOOTSTRAP / RUNTIME DEFAULTS]
[10 PLATFORM / PROVIDER INSTRUCTIONS]
[20 OPERATOR CONSTITUTION]      ← F1-F13, APEX Reality Kernel, AAA sovereignty
[30 AGENT IDENTITY + ROLE]      ← SOUL.md + HERMES_IDENTITY.md
[40 SKILL INSTRUCTIONS]
[50 SESSION CONTEXT]
[60 MEMORY / RETRIEVAL CONTEXT]
[70 TOOL + MCP CONTEXT]
[80 USER REQUEST]
[90 DELEGATION / SUBAGENT CONTEXT]
[99 OUTPUT + AUDIT WRAPPER]
```

For each bracket, output exactly these fields:

```
INPUTS received · TRANSFORMATION or selection rule · OUTPUT passed onward
AUTHORITY owner · DATA classification · TOOL authority permitted
FAILURE MODE · EVIDENCE class and location/hash where safely available
```

If a bracket is NOT evidenced (no file found, no port answering, no process alive), say `state: ABSENT — evidence UNKNOWN` and move on. Do not fabricate presence.

## Evidence-class taxonomy — six labels, nothing else

| Label | Meaning |
|---|---|
| PROBED | Live runtime evidence obtained this session via tool call |
| CONFIG-DERIVED | Found in active configuration or loaded source file |
| LOG-DERIVED | Found in a timestamped invocation/audit receipt |
| INFERRED | Conclusion from indirect evidence (mark weak) |
| DECLARED | Documentation, skill text, banner, or registry claim only |
| UNKNOWN | Insufficient evidence — NOT PASS, NOT FAIL |

A statement with no label attached is a defect, not an audit.

## Section-I machine-receivable JSON — required schema fields

```json
{
  "audit_id": "<uuid or sha prefix>",
  "timestamp": "<ISO-8601 UTC>",
  "mode": "read_only",
  "scope": ["prompt_scaffold", "mcp", "gates", "federation_flow"],
  "runtime": {
    "hermes_version": "<from `hermes --version`>",
    "local_commit": "<git_commit short>",
    "upstream_commit": "<upstream_commit short>",
    "execution_identity": "REDACTED"
  },
  "visibility": {
    "prompt_scaffold": "full|partial|none",
    "federation_flow": "full|partial|none"
  },
  "prompt_layers": [{"rank":0,"name":"...","state":"probed|config_derived|log_derived|inferred|declared|unknown","active":true,"enforcement":"...","evidence_ref":"<path:line or null>"}],
  "mcp_summary": {"declared":0,"probed":0,"healthy":0,"ready":0,"degraded":0,"down":0,"disabled_intentional":0,"unknown":0},
  "gate_tests": [{"gate":"...","result":"pass|fail|unknown","side_effect_free":true,"evidence_ref":"<path:line or null>"}],
  "holds": ["...F13 binary questions deferred to sovereign..."],
  "top_risks": ["..."],
  "verdict": "green|amber|red|unknown",
  "confidence": 0.0
}
```

`confidence` is your honest estimate of evidence completeness, not a goodness rating. Cap at 0.95 unless every section is PROBED.

## Pitfalls — the recurring failure modes

**1. Calling `hermes_mutation_gate.py` "the gate."** It is DEPRECATED (header: `DEPRECATED (2026-08-09) · NOT WIRED · library only`). The live gate is `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py` wired in the active profile's `config.yaml` under `hooks.pre_tool_call`. Always find the wired file, not the canonical-looking one.

**2. Reporting `healthy` when status is `stdio_present`.** `stdio_present` means a launcher script is configured and a smoke test passed — NOT that the server is actually answering live calls. Use the documented status vocabulary; do not soften.

**3. Treating a service in `running` state as "governed."** A `systemctl` running state proves the process started, not that any gate is bound. The audit separates these on purpose. Combine: process UP + hook wired + receipt trail present → governed. Anything less → "process up, gate status UNKNOWN."

**4. Quoting secrets into the audit.** Redact `[REDACTED]`; declare category only (`api_key | oauth_token | pg_password | bws_cache | ...`). Authenticated capability map (`/health` `capability_map.providers`) reports status, never values — keep that discipline.

**5. Reporting "all safe" or "fully governed."** Forbidden phrases. The verdict is one of `green | amber | red | unknown`. UNKNOWN is the honest answer when evidence is partial; downgrade, do not promote.

**6. Skipping sections B/C/D/E because "nothing to say."** Every section is mandatory. If a bracket is absent, write `state: ABSENT` with `evidence: UNKNOWN`. Do not collapse.

**8. Probing past the 12-step boundary.** Past step 12 you are decorating. The audit's authority is its probe discipline; over-probing wastes attention budget and the audit loses shape.

**9. Using bash heredoc / cat-pipe-to-python for live data extraction.** Tirith flags these as `[HIGH]` risk. Read the file with `read_file` or write a small script to disk first, then run it.

**10. Reporting "ingest" or "sent" without naming state.** PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED. State-transition discipline applies to the audit itself.

## Output format

Plain text with the section headers `A.` through `I.` as the user typed them. Tables are allowed inside sections — they are the spec, not decoration. No opening greeting, no closing moral, no "let me know if..." footer.

The audit MUST end with section I (Honest Gate Map + Recommendations). Section I is the only section where the sovereign gets a binary they can act on. Do not omit it.

## Companion skills

- `chokepoint-enforcement-audit` — for single-gate audits (one chokepoint, one mechanism)
- `governance-ops` — for "is this control real?" routing
- `live-probe-audit-pattern` — for narrative-vs-state probe hygiene
- `audit-repo-reality` — for repo-state audits

## Anti-collapse

A /000 INIT audit is NEVER a 4-bullet summary. If you find yourself wanting to write "all safe, governance in place, here are the top three risks" — you have collapsed the section structure. Re-expand to A–I.