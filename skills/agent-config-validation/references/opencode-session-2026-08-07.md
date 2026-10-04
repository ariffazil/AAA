# OpenCode + arifOS incident — 2026-08-07

Concrete reproduction recipe for the "Configuration is invalid" + "cannot spawn multi agent" cascade that hit the federation on 2026-08-07. Both symptoms had the same upstream cause but different surface errors.

## Timeline (UTC)

- **03:44–03:46** — arifOS (:8088) entered systemd restart loop. Root cause: `/opt/arifos/app/arifosmcp/resources/refusal_surface.py` became `root:root 600` after a deploy, unreadable by the `arifos` service user → `PermissionError` on import → service crashed → systemd tried to restart → loop.
- **~04:00** — user opened OpenCode TUI. Welcome banner loaded, plugins wired, models listed.
- **~04:05** — user pasted screenshot asking "Why my terminal cannot spawn multi agent?" Symptom: subagent task dispatch hanging / "session not bound".
- **~04:06** — sibling agent pasted incident report (incident-resolved ticket) for the arifOS restart loop.
- **~04:08** — diagnosis: arifOS was in restart loop, KernelBridge plugin hooks firing arif_init on every TUI session → connection refused → session never bound → subagent task denied.
- **~04:10** — chown + chmod fix applied to refusal_surface.py, `systemctl reset-failed`, restart. /health returned 200.
- **~04:12** — user asked "Call Apex judge to evaluate your solutions". `arif_judge` called via curl → returned `effective_verdict: HOLD` with `reason_code: UNMEASURED_INPUT`. This was F11+F13 working as designed (anonymous curl = no SCT = no seal authority), not a flaw in the patch.
- **~04:14** — user pasted Kimi Code TUI screenshot showing `Model: MiniMax-M3`. I incorrectly patched `/root/.kimi-code/config.toml` to `managed:kimi-code/kimi-k3` thinking it was a vendor mismatch. User corrected: "Kimi code is multi modal, it's dynamics." Reverted to `minimax-coding-plan/MiniMax-M3`.
- **~04:18** — user reported "Configuration is invalid" error from OpenCode. Diagnosis: `_last_updated` + `_patch_summary` keys appended by sibling FED-wiring patch were unknown to OpenCode's strict schema.
- **~04:20** — applied fix: stripped the two `_`-prefixed keys, verified `opencode models` returns 1600+ entries, `opencode debug config` resolves cleanly, 5/5 plugins PASS smoke test.

## Root-cause matrix

| Symptom | Surface cause | Root cause | Fix |
|---|---|---|---|
| OpenCode "Configuration is invalid" | `_last_updated`, `_patch_summary` unknown keys | Sibling patch appended audit metadata to JSON root | Strip keys; use sidecar `.meta` file for future audit |
| Multi-agent spawn failure | Subagent task denied | arifOS :8088 in restart loop → KernelBridge session bind fails | chown arifosmcp resources to arifos:arifos; reset-failed; restart |
| Kimi Code "wrong model" | Welcome banner shows MiniMax-M3 | Not a bug — Kimi Code is multimodal; user picks via `/model` at runtime | None — revert any patch |

## Files involved

- `/root/.config/opencode/opencode.json` — schema-forbidden keys
- `/opt/arifos/app/arifosmcp/resources/refusal_surface.py` — ownership drift
- `/root/.kimi-code/config.toml` — `default_model = "minimax-coding-plan/MiniMax-M3"` (intentional, do not patch)
- `/root/.tmux.conf` — missing `set -g extended-keys on` (Enter key not registering in tmux)

## Backups (still on disk)

- `/root/.local/share/arifos/snapshots/2026-08-07-soul-strip/` — SOUL/AGENTS state pre-strip
- `/root/.local/share/arifos/snapshots/2026-08-07-opencode-fix/opencode.json.pre-fix.bak` — OpenCode config pre-fix (60,959 bytes)

## arif_judge verdict shape (for the next session)

When calling `arif_judge` directly via curl without first binding a session:

```json
{
  "effective_verdict": "HOLD",
  "authority": {"reason_code": "UNMEASURED_INPUT"},
  "verdicts": {
    "substrate": {"state": "HEALTHY"},
    "session":   {"state": "OBSERVE_ONLY", "evidence_reference": "actor_verified=False"},
    "action":    {"state": "NOT_EVALUATED"},
    "receipt":   {"state": "UNSEALED"}
  },
  "nine_signal": {
    "delta": {"state": "RETAK", "en": "CRACKED"},
    "psi":   {"state": "SYUBHAH", "en": "DOUBTFUL"},
    "omega": {"state": "BIJAK", "en": "PRUDENT"}
  }
}
```

`HOLD` here means "I refuse to seal unsigned work" — not "the patch is bad". To get SEAL-grade verdict, bind a session first via `arif_init(actor_id="ARIF")` and pass the resulting SCT.

## Lesson encoded

This incident is now codified in the parent skill `agent-config-validation` — three recurring traps (schema-rejection, json round-trip loss, dynamic-model confusion) plus the multi-agent-spawn chain that ties them to arifOS kernel health.