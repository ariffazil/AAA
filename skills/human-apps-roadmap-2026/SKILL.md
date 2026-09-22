---
name: human-apps-roadmap-2026
description: "Canonical ranked roadmap of human-benefit applications for Arif (briefing, WhatsApp assistant, email copilot, finance radar, health mirror, work copilot)."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Human-Benefit Apps Roadmap (canonical pointer)

**Full research:** `/root/docs/human-benefit-apps-2026.md` (2026-09-16)
**One-line thesis:** infrastructure-rich, application-poor — assemble live lanes into human surfaces instead of adding more MCPs.

## Ranked build order

1. **Morning Briefing** (Telegram 07:00 MYT) — all lanes already LIVE (gws calendar/email, WEALTH market, WELL, search); pure assembly cron. Build first.
2. **WhatsApp group assistant** — `whatsapp-mcp-plus` (maintained, read-only default, whitelist, confirm-to-send) or WAHA. Ban risk real: spare number, read-only, 1-2 groups. Biggest Malaysian daily time sink.
3. **Email triage + drafts-only copilot** — gws Gmail live; Outlook personal via `outlook-mcp` with `allow_categories=["mail_drafts","mail_triage"]` if MS account exists. PETRONAS corporate data = F13 policy gate.
4. **Finance radar** — BNM API Kijang (live official data) + WEALTH organ + receipt-photo logging; Open Finance MY (PayNet, banks+EPF) mandatory sharing from 2027-01-01 = future real bank data. TNG: no consumer API.
5. **Health mirror** — needs only Arif's `biometric.full` consent + Google Fit watch sync (cron exists). WELL is blind without it.
6. **PETRONAS work copilot** — meeting prep, GEOX→report drafting, learning digests. Corporate-data policy gate first.
7. **Home Assistant MCP** — official, local, free; wire when first smart device arrives.
8. **Voice-first Hermes** — ASR+TTS components all exist; assembly job.

**Rejected (final):** adult content (F5/F6), gambling/prediction signals, ToS-violating scraping for gain.

## Joy lane (added 2026-09-16 evening)
Evidence from Arif's own calendar: Mr Olympia 2026 💪 (Sept 22–27 LV — NEXT WEEK; Finals MYT Sat/Sun ~9-10am, OlympiaTV PPV) + KL City Duathlon 2026 (he races!). Tools: `davidmosiah/strava-mcp` + `delx-wellness-hermes` (9 wellness connectors: Garmin/WHOOP/Oura/Fitbit — feeds WELL organ + duathlon coach). Music: `pete-builds/mcp-spotify` (remote Docker :3703, multi-agent) or `pikaro/spotify-mcp` (100+ tools, PKCE). F13: stream Siti Nurhaliza yes, clone her voice never. Muscle-culture appreciation = joy lane; explicit kink = rejected (F6).

## Sleep + micro-joy lane (added 2026-09-16 night — "sleep is happy as well")
Sleep = joy lane (sovereign call), full research in `/root/docs/human-benefit-apps-2026.md` S1–S4. Anchors: Windred 2024 (sleep regularity beats duration, 20–48% mortality delta) · Lajunen 2023 (duration ~30% of happiness variance) · Seligman 2005 (3 Good Things → 6-month happiness gains) · White 2019 (≥120 min/wk nature threshold) · Sturm 2020 (15-min weekly awe walk) · NASA 26-min nap (+~50% alertness). Features, ZERO new MCPs: briefing sleep line joy-framed + bedtime-consistency streak · wind-down nudge + caffeine cutoff (~16:00) on existing 22:00 digest · "3 baik hari ini" (3GT) = one line on existing digest, shippable tonight · Menu Suka (dopamine menu, Mayo/ADDitude pattern) = pre-decided micro-joy starters seeded from his lanes · nature-120 counter + awe-run suggestions once Strava live (KL: Perdana Botanical, KLCC Park, Titiwangsa, FRIM) · nap window via WELL `log_recovery_event(nap)` (exists) · sunrise lamp = T3 his call. **S3 SHIPPED 2026-09-16 01:10 MYT** (witness PROCEED_S3, conf 0.84): digest human block live in `arifflow_digest.py` · `cron-deliver.sh` revived at `/root/.hermes/scripts/` (was phantom since zen-20260912 — nightly digest delivery was silently dead) · reply capture = Hermes skill `WELL-3baik-log` (`3baik:` prefix → `/root/WELL/state/3baik_log.jsonl`) · policy `/root/WELL/state/human-benefit-sleep-joy-v1.json` ACTIVE · population effect sizes = PLAUSIBLE for Arif individually, learn from his data.
