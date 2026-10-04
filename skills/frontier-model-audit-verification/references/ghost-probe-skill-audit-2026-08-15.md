# Ghost-Probe Skill Audit — 2026-08-15

Session: Arif pasted an external "Hermes probe" report recommending a
72 → 10 skill prune with two "critical findings" (Telegram gateway DOWN 6
weeks; curator never ran, run_count: 0). Both findings, and the inventory
itself, were falsified by one-line probes against the live surface. No
prune was executed. The session pivoted into a real gap analysis that
produced the my-reality adapters.

## Claims vs live state (all reproduced)

| Probe report claim | Live surface probe | Result |
|---|---|---|
| "72 bundled skills" | `find <trees> -name SKILL.md \| wc -l` | 476 (live profile) / 442 (~/.hermes) / 289 (bundled) — 72 matches nothing |
| "Telegram DOWN since 2026-07-05 (invalid token)" | `gateway_state.json` → `platforms.telegram.state: connected`, updated that hour; `ps` gateway alive; `grep -c 'response ready: platform=telegram' logs/gateway.log` → 1,769 | REFUTED — and the report arrived VIA Telegram |
| "Curator run_count: 0 — never ran" | `cat skills/.curator_state` (both profiles) | run_count: 1 on each; default profile ran 2026-08-14, marked 36 stale |
| "Zero real traffic" | `state.db` messages table | 64,348 messages across ~9 days |

## Why the report was seductive

Its two "critical findings" both justified its own recommendation ("no
traffic → no evidence → prune is unsafe / curator never ran"). The
architectural analysis (abstractions over implementations, github-relay,
fi-dispatch) was sound — built on false premises. Sound reasoning over
unverified state is still a fabricated audit.

## Detection tells (generalized)

1. **Round-number inventory** — live systems don't have exactly 72 of anything.
2. **Dead-channel paradox** — report about a dead channel that reached you
   through that channel probed a different surface.
3. **Load-bearing critical findings** — a finding that anchors the report's
   recommendation is the MOST suspect claim, not the anchor. Re-probe it first.
4. **Specific state-field claims** — "run_count: 0" is cheap to reproduce;
   never accept it unread.

## The four-state gap classification (applied)

Before declaring a missing capability, resolve to one state — fix classes
differ radically:

| State | 2026-08-15 example | Fix |
|---|---|---|
| Absent | prayer / weather / AQI adapters | build |
| Exists-disabled | (none found) | enable |
| Wired-but-broken | STT: pipeline ON (`stt_enabled` default true), faster-whisper never installed, no provider keys | `pip install faster-whisper` — no gateway restart (transcription_tools.py rechecks `find_spec` per call; verified ms-audio transcribed 3.9s CPU) |
| Hidden/dormant | `malaysia_adapters.py` (403 lines, BNM/OpenDOSM/Bursa) — 0 importers since refactor | activate/wire |

## Traffic-derived gap analysis (the productive pivot)

Telemetry from `state.db` (5,449 user msgs scanned, keyword counts only):
solat 178, petrol 149, cuaca 26, voice/audio 450+ — against skill tree
grep: zero Malaysia reality surfaces. Demand side was real even though the
probe report's premise was fake. 941 web_search calls in 9 days = humans
paying round-trip cost for what a keyless API answers in one call.

## Live-verified API quirks (for my-reality maintenance)

- Aladhan: 302 redirect — needs `-L` / urllib follow. method=17 (JAKIM) == method=20 times for George Town.
- BNM exchange-rate: rate object nested `data[].rate.middle_rate`, NOT `data[].middle_rate`.
- BNM Kijang Emas + exchange-rate: require `Accept: application/vnd.BNM.API.v1+json`.
- date.nager.at publicholidays/2026/MY → HTTP 204 (no 2026 data yet) — don't build on it.
- data.gov.my weather endpoints → 404 at audit time; council-cited URLs ≠ live. Use Open-Meteo.
- Terminal guard: commands that mention gateway restart keywords are blocked from inside the gateway session ("would kill this command"); use read-only state files instead.

## Outcome

- Prune: NOT executed (premises falsified).
- STT wire: repaired + verified end-to-end.
- `my-reality` skill forged: 5 adapters (prayer/weather/aqi/fx/gold), all live-verified, keyless.
- apex-judge isolate returned HOLD on the git commit (additive artifacts verified, seal awaits F13).
