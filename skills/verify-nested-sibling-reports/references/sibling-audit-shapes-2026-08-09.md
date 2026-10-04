# Sibling-report audit shapes (2026-08-09)

Five shapes from auditing two sibling reports in one session — OpenClaw's APEX SWOT
(federation-state report, ~80% accurate, 1 factual error, 1 identity drift) and an
MCPJam agent-wiring report (infra report, 19/19 clean). Same machinery for both:
enumerate load-bearing claims → batch live probes in parallel → verdict table.

## 22.1 Constitutional lane re-mapping inside sibling self-reports

Pattern: a sibling's status report re-describes federation lane assignments — its
own or other agents' — differently from the ratified grammar. 2026-08-09 case:
OpenClaw self-identified as "333-AGI · Δ MIND" (claiming think/route/execute) and
mapped Hermes as "555-ASI." The ratified Constitutional Grammar V1 (2026-08-08)
reads OpenClaw=SENSE, Hermes=COORDINATE.

This is not automatically fabrication — the grammar may have evolved — but a lane
re-map inside a sibling report is a **constitutional claim that needs a ratified
source**. Accepting it silently is how role creep becomes doctrine.

Probe recipe:
1. State the ratified mapping from memory/canon (e.g. Constitutional Grammar V1).
2. Grep canon for a post-ratification update:
   `grep -rl "CONSTITUTIONAL_GRAMMAR\|lane grammar" /root/AAA/governance/ | head`
3. If no ratified update exists: flag "identity drift — requires sovereign
   ratification." Do not adopt the sibling's mapping in your reply.

Reply shape: "OpenClaw self-reports 333-AGI; ratified grammar says SENSE. Lane
re-map with no cited ratification = drift flag, not ground truth."

## 22.2 "X is a bare process" claims — probe systemd, not just ps

Pattern: a report lists fragile services ("Hermes/WEALTH/WELL are bare processes,
not systemd"). These claims are verifiable in two commands and are frequently wrong
for exactly one of the listed services.

Probe recipe:
```bash
ps aux | grep -iE "[X]" | head -5                                   # what actually runs
systemctl list-units --type=service --state=running | grep -iE "X"  # what systemd manages
```

A main process running outside systemd while a `<name>.service` unit is active is
ambiguous — check what the unit actually runs (`systemctl cat <name>.service` →
ExecStart) before calling it managed. 2026-08-09 result: Hermes gateway (PID 666329,
`hermes gateway run --replace`) = bare ✓; WEALTH `server_federated.py` = bare ✓;
WELL = **systemd-managed** (`well.service` active) — the report was wrong on 1 of 3.

## 22.3 "All health endpoints returned 200" — HTTP code ≠ health

HTTP 200 with a body of `{"status": "degraded", ...}` still returns 200. A report
citing only status codes is technically true but semantically empty. Read the JSON
body: `status`, `deployment_drift_status`, `kernel_verdict`. Same family as §14.3
(rules not surfaced in /health) — the probe shape is weaker than the claim.

## 22.4 Verifier harness false negatives — check keys, not substrings

When YOUR OWN probe script reports failure, dump the raw payload before concluding
the endpoint is broken. 2026-08-09 case: my WELL :18083 initialize probe flagged
"INIT returned ERROR" because the script did `if "error" in resp` — and the valid
`result` payload contained the substring "error" inside nested capability text.
WELL was fine; the harness was wrong.

Rule: parse the JSON and test for a **top-level `"error"` key**, never substring
match. When your harness contradicts a sibling's "all green" claim, the tiebreak is
the raw payload, not either narrative.

## 22.5 The clean-report shape (positive control) + skill-mesh claim verification

Not every audit finds inflation. The MCPJam wiring report verified 19/19 with zero
fabrication. Its shape is the positive control for §6's "useful report" column:
structured tables with file paths, timestamps, file modes, a receipt path, no
ceremonial flourish, no ΔS claims, and every row falsifiable in <10s. Recognize
this shape and say "high quality, verified" without manufacturing caveats.

One claim class it carried needs its own probe map: **"skill X synced to all N
agents."** The 7-agent mesh paths (verified 2026-08-09):

| Agent | Skill dir(s) |
|---|---|
| Grok | `/root/.grok/skills/` |
| Claude Code | `/root/.claude/skills/` |
| Codex | `/root/.codex/skills/` |
| OpenCode | `/root/.arifos/agents/opencode/skills/` |
| Hermes | `/root/.hermes/skills/` + `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/` |
| Kimi Code | `/root/.kimi-code/skills/` |
| OpenClaw | `/root/.openclaw/workspace/skills/` |

Trap: Kimi also has `/root/.arifos/agents/kimi/skills/` (other skills live there)
but the mesh-synced copies land in `/root/.kimi-code/skills/` — searching only the
`.arifos` path yields false MISSING. Canonical paths live in
`/root/AAA/skills/scripts/skill-mesh-sync.sh`; read the script when in doubt.

## 22.6 Note on VAULT999 hash-chain counts in sibling SWOTs

OpenClaw's APEX SWOT cited "VAULT999: immutable hash-chained memory" as a strength.
Live probe (2026-08-09): 44,043 entries, only 11 carry both `hash` and `prev_hash`
(0.025% coverage, down-ratio from §17's 11/37,016). The §17 two-probe rule applies
whenever a sibling SWOT lists VAULT999 integrity as a strength — architecture true,
enforcement false until coverage is measured.
