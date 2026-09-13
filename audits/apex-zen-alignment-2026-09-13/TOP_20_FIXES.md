# TOP 20 FIXES — APEX-ZEN Sweep v1
> Ranked by impact × expected reduction in **Discussion Debt (DDR)** vs complexity/risk. Session `SEAL-42dad7d3d9334310`.
> Scale: H/M/L. DDR = expected discussion-debt reduction.

| # | Fix | Impact | Cplx | Risk | DDR | How |
|---|---|---|---|---|---|---|
| 1 | **Schedule Layer-2 telemetry** (cron nightly; kimi dir first, then all harnesses) | H | L | L | H | `cron: 0 23 * * * python3 /root/AAA/scripts/apex-zen-telemetry.py --input-dir <dir>` per harness |
| 2 | **Calibrate detectors** (assistant-role filter; exclude system/tool payloads; dedupe) | H | M | L | H | edit `apex-zen-telemetry.py` scan loop; re-run same session for delta proof |
| 3 | **Layer-4 minimal consequence router** (weekly breach → session-start injection + FQ coupling) | H | M | M | H | read `APEX-ZEN-CONSEQUENCE-LADDER.md`; wire score→reminder hook |
| 4 | **Multi-harness transcript adapters** (claude-code, opencode, codex, qwen formats) | M | H | L | M | normalize to the collector's text interface |
| 5 | **A2A harness executor bridge** (warga → coding agents real execution; NATS inbox poller or hermes-gateway route) | H | H | M | M | extend `/root/AAA/a2a-server`; canary = kimi WCANARY round-trip |
| 6 | **Land seed-test alignment** (Agentic CI 7 assertions) | M | M | L | M | align `seed-agents` canonical list (PR #185 direction) |
| 7 | **Branch-protection truth** (stop silent bypass of `npm ci` check; fix or retire the rule) | M | M | L | L | align with issue #182 dependabot-guard rework |
| 8 | **Docs refresh pack** (CODER_FEDERATION_MAP current-FI; CROSS_HARNESS reconciliation; AGENT_INTELLIGENCE FI-004) | M | L | L | M | content staged this session; small PRs |
| 9 | **README SOT-MANIFEST restamp** (live_commit after push train) | L | L | L | L | update `live_commit` + `last_verified` |
| 10 | **Review PRs #186 / #178** (qwen lab extension; @mcp-b/global major bump) | M | L | L | L | diff review + checks; merge or hold with reason |
| 11 | **Runtime session hygiene** (retention + ignore audit for `agents/*/runtime/**`) | M | M | L | L | define retention; move from git to disk-only |
| 12 | **DCR source of truth** (ratify definition; wire arifFlow `flow_gov_events`) | M | L | L | M | F13 ratify definition; small collector patch |
| 13 | **FI-011 Continue decision** (izin TBD since 2026-08-21; use or decommission) | L | L | L | L | F13 decision; registry entry update |
| 14 | **Rate-limit weekly scorecard publish** (cockpit surface) | M | M | L | M | cron + cockpit panel |
| 15 | **Telemetry privacy/scope check** (transcripts → VAULT999 path; sanctuary rules) | M | L | M | L | review before G1 scheduling |
| 16 | **Gemini residue sweep** (unregistered binaries + config refs after FI-010 death) | L | L | L | L | config tidy; registry already updated |
| 17 | **FI-009/FI-007 version notes in cards** (1.2.2 / 1.0.30) | L | L | L | L | cards + registry consistent |
| 18 | **Archive sweep** (`agents/*/_archive*` + `_superseded` stale dirs → A-ARCHIVE) | L | M | L | L | flag list; archive move under F1 |
| 19 | **flow_ingest Verify receipts** for each sealed task (raise FQ balance systematically) | M | L | L | L | plugin hook on task close |
| 20 | **Ratify targets after 7 days** (CD<0.05, DD<2, IAR>0.8, DCR>0.9 → F13) | M | L | L | M | F13 ritual after series exists |

## Execute-next trio (highest leverage, lowest risk)
1. #1 + #2 + #15 (telemetry becomes real, calibrated, scoped) → creates the missing WITNESS edge.
2. #3 (consequence router) → closes the governance loop.
3. #5 (warga→coder execution bridge) → converts registration into usable capability.

**FORBIDDEN (per sweep):** no new doctrine, no new floors, no new abstractions. All 20 items are wiring, calibration, cleanup, or ratification — zero new governance layers.
DITEMPA BUKAN DIBERI — 2026-09-13
