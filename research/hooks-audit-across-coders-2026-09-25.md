# Hooks Federation Audit Across Coders — Phase B Probe (2026-09-25)

> **Status:** PHASE-B PROBE COMPLETE. Single-session live audit. Not a federation-wide canonical.
> **Closes:** Loop L05 from `/root/AAA/blueprints/HOOK-FEDERATION-STANDARD-DRAFT-v0.md` §7.
> **Method:** Read-only source + filesystem probe. No execution, no mutations.
> **Sandbox limit:** loopback HTTP blocked (`policy=never`); TCP-reachable truth comes from
> `/root/.hermes/MCP_HEALTH.json` (aged ~10h at survey time), not live curl.

---

## 1. Coders inventory (live snapshot)

7 coders cited in the draft §3. Live filesystem evidence:

| Coder | Hooks dir location | Status this session |
|---|---|---|
| **OpenCode** | `/root/.opencode/hooks/*.ts` | UNVERIFIED in this sandbox (`.opencode` not enumerated) |
| **Codex CLI** | `/root/.codex/hooks/*.py` | DIRECTORY EXISTS, contents enumerated below |
| **Qwen** | `/root/.qwen/hooks/*.sh` | UNVERIFIED (`.qwen` not probed; cited from draft) |
| **Gemini / Kimi / Grok** | (per draft) `.gemini`, `.kimi`, `.grok` | Grok present at `/root/.grok` but hooks dir absent (matches draft "hooks dir empty / config absent") |
| **OpenClaw** | `/root/.openclaw/hooks/*.md` | gateway, not coder — draft already classifies as N/A |

## 2. Codex hook surface — concrete enumeration (this session)

```
$ ls /root/.codex/hooks/
aaa_session_witness.py
f2-receipt.py
(2 hooks)
```

Per `HOOK-FEDERATION-STANDARD-DRAFT-v0.md` §3 row "Codex":

| Spine event | Codex state |
|---|---|
| 1. session-create / session-open | ⚠️ not wired |
| 2. pre-tool-call (gate) | ⚠️ not wired |
| 3. post-tool-call (receipt) | ⚠️ not wired (referenced in draft) |
| 4. subagent-spawn (envelope) | ⚠️ not wired |
| 5. session-reset / carry-forward | ⚠️ not wired |
| 6. exit (seal / clean-up) | ⚠️ not wired |

The two Python files present (`aaa_session_witness.py`, `f2-receipt.py`) are present but **not
wired into any of the 6 spine events** for this Codex runtime — match the draft's "5/7 coders
partial" classification for Codex.

## 3. Live MCP-routable coder-receivers (cross-check)

`/root/.hermes/MCP_HEALTH.json` shows n=30 MCP servers, of which 18 healthy + routable.
None of the 18 are coder **hook surfaces** — they are organ surfaces (arifos, frame, wealth,
geox, well, claim-ledger, doc-tables, filings, media-ingest, numeric-audit, session-federation)
or external services (context7, deepwiki, firecrawl, zai_reader, zai_search, fed, hermes-mcp).
Conclusion: the hook-vs-MCP distinction is clean — coder hooks fire inside the coder process,
organ MCPs are external services. **Spine #1 (session-create)** is the boundary that hooks
MCP coordination.

## 4. Where to wire next (one Phase-B probe — single coder)

The cheapest single-coder closure to prove the spine works end-to-end is **Codex CLI spine #4
(subagent-spawn envelope) + spine #5 (session-reset carry-forward)**, because:

- Codex CLI is THIS runtime; hook code already exists in `/root/.codex/hooks/`.
- Other coders (OpenCode, Qwen) require cross-machine wiring.
- The two un-wired hooks (`aaa_session_witness.py`, `f2-receipt.py`) are partial implementations
  of these spine events.

Proposed ≤15-minute probe:

1. Add a `codex-config.toml` `[hooks.session-reset]` entry pointing to `aaa_session_witness.py`.
2. Run a single Codex session reset.
3. Check `/root/.hermes/carry_forward.json` for a new `anchors` entry with `trace_id`.

If the probe produces the expected anchor, L05 rows for Codex flip from `5/7 NOT wired` to
`1/7 COMPLETE (OpenCode per draft) + 1/7 PARTIAL-UPGRADE (Codex)`.

## 5. Honest unknowns

- OpenCode, Qwen, Gemini, Kimi, Grok coders: **not probed in this session** (out of `.codex/` scope).
- Live hook execution cannot be replayed in this sandbox (no `opencode`, `qwen-code`, `kimi-code`
  command runs).
- The hooks here are still textual — Codex's T3 hardening path (L09 scar P0.5 fix) is layered
  on top, not the hook wiring.

## 6. Next action (this doc proposes, does NOT execute)

If Arif approves this Phase-B probe, FI-005 will:

1. Write `/root/.codex/config.d/hooks-session-reset.toml` with the `session-reset` block.
2. Run one probe Codex session with explicit reset.
3. Verify carry_forward anchors + `trace_id`.
4. Close L05 row in `HOOK-FEDERATION-STANDARD-DRAFT-v0.md` §7 with the probe receipt.

Expected L05 closure time: 10–15 min. Single-coder. No F13 needed (T1 AUTO).

DITEMPA BUKAN DIBERI ⚒️
