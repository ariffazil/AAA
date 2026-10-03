---
title: "Deferred Questions — Held for Future Sessions"
subtitle: "Items raised but not actioned in 2026-10-03 cross-domain literature review session"
date: "2026-10-03"
status: "HELD — pending Arif's F13 binary decision"
---

# Why this file exists

The 2026-10-03 cross-domain literature review session produced the EUREKA synthesis (`04-eureka-cross-domain-synthesis.md`). Several other threads were raised mid-session and **deferred** so the EUREKA could complete. This file lists them so a future agent doesn't have to re-derive the context.

---

# Deferred Threads

## D1. Reality Engineering / AREP protocol research plan

**Originating message:** ~22:00 SGT, 5-bullet research plan about analyzing `ZEN_OF_REALITY_ENGINEERING.md`, AREP contracts, autonomous loop mechanics, failure tolerance governance, and implementation strategies.

**Arif's F13 binary decision:** "Habiskan literature review dulu (Recommended)" — held.

**Subsequent elaboration:** ~22:05 SGT, 3-practical-advantage follow-up (Elimination of Blind Execution / Guaranteed Safety Boundaries / True Autonomy). HERMES later refused to amplify this as narrative completion.

**Status:** Held. Implementation work for AREP / Reality Engineering is *not* the literature review. The federation already has runtime evidence that 4/6 floors FAIL, 7% shadow receipt, 78/122 A-FORGE tools unmapped — pursuing implementation of "Guaranteed Safety Boundaries" without first resolving runtime gaps is the canonical narrative-completion defect.

**Recommendation for next session:** Treat AREP / Reality Engineering as a *gap-fixing* exercise, not an architecture-rebuild. Specifically:
1. Land the 4/6 floors FAIL → ≥5/6
2. Bring 7% shadow receipt → ≥25%
3. Map the 78/122 A-FORGE tools to the 8 canonical verbs
4. *Then* talk about AREP

Without (1)-(3), the AREP stack is built on a foundation that does not support the load. The blueprint's gap report confirms this is the current state.

## D2. Shadow-cron chmod + flow_entity_report replacement

**Originating message:** earlier in 2026-10-03 session (from a subagent), proposing:
- `chmod +x` on `shadow_geometry_cron.sh`, `agent-cockpit/cockpit.sh`, `attention_signal.py` (973 missed cycles)
- Replace hardcoded FQ table in `shadow_geometry_comparison.py` with a live `flow_entity_report` query
- Watch one full cycle

**Arif's response:** approved initially, then redirected to Caddy edge hardening. Now held in "still outstanding" per the latest session message.

**Status:** Queued, awaiting Arif's F13 binary to proceed. The fix is reversible (one chmod + a config edit); but without it, the loop that detects shadow continues to publish fiction every 6 hours.

**Recommended execution order:**
1. Backup the three scripts (F1 AMANAH)
2. `chmod +x` on the three
3. Edit `shadow_geometry_comparison.py` lines 131-170 to call `flow_entity_report` instead of literals
4. Re-run manually once, observe one cycle, capture receipts
5. If cycle is clean, leave cron on; if not, hold and report

**Risk:** If step 3 fails (e.g., `flow_entity_report` returns nothing), the loop will publish empty/fictional data. Per F11 AUDITABILITY, that's worse than no loop at all.

## D3. 5 CHRON predictions (A/B/C/D/E branches) — calibration fix

**Originating message:** ~22:00 SGT from a subagent. Registered 5 predictions:
- A: Gosplan attractor (0.55, verify 2027-01-15)
- B: Witness premium (0.35, verify 2027-03-31)
- C: Coordination w/o agreement (0.25, verify 2027-06-30) — TENTATIVE
- D: Platform capture (0.45, verify 2026-12-31)
- E: Institutional durability (0.30, verify 2027-09-30) — TENTATIVE

**Issue raised:** `chron_create_event` has no probability field; amplitudes entered as 0.5 default and came out calibrator-adjusted. Discrimination gone; TENTATIVE branches received *higher* confidence (0.5412) than PREDICTED (0.4942). Brier will barely move when C resolves false.

**Proposed fix:** one field — let the event carry the amplitude into `confidence_proposed`. Difference between a calibration trail and a formality.

**Status:** Held. The fix is a one-line change to the CHRON event schema. Calibration is foundational to F8 GENIUS / F11 AUDITABILITY.

## D4. Shadow YAML schema fix — `last_confirmed` + `evidence_count`

**Originating message:** from earlier 2026-10-03 audit (in main session). The 122-shadow-entry audit identified that no YAML has `last_confirmed` field and none has numeric `evidence_count`. The rule "promote HYPOTHESIS→CONFIRMED at N≥5" exists in `MODEL_SHADOWS.md` but has no counter to reach 5.

**Status:** Held. The fix is a schema migration across 8 model + 8 harness shadow YAMLs. Per F2 TRUTH, this is required for falsification to be executable.

**Tied to D2:** the schema fix and the cron chmod are the same defect class — internal-coherence without reality-contact. Either both get fixed, or both remain shadow.

## D5. Cedar bridge fail-OPEN stub

**Originating message:** from earlier 2026-10-03 audit + cross-check. `arifos_policy/cedar_bridge.py` = 27 lines, `enabled: False`, `evaluate()` always returns `ALLOW override:True`, not imported by `server.py`.

**Risk per audit:** fail-OPEN is *worse* than absent — every call to `evaluate()` says "yes" unconditionally, and any downstream code that trusts the verdict is silently granted a false-positive.

**Status:** Held. Two paths:
1. Remove the stub entirely (safer — `enabled: False` already so it's a no-op, but the code still exists as a future attack surface)
2. Wire it properly to the 13 floors (the blueprint's prescription; larger change)

**Recommended first action:** read the 27 lines, decide whether it's actually imported by anything, and if not, delete it. If imported, set `enabled: True` only after wiring to actual floor evaluation. Per F1 AMANAH, no behaviour change without explicit Arif approval.

## D6. Caddy alias /api/organs/* on mcp. (86,941 B, 9 routes)

**Originating message:** ~22:10 SGT from Caddy edge session. /api/organs/* on mcp. still open, including /api/organs/arifos/tools at 48,273 B of full schema. **Deliberately left open** because /var/www/html/mcp/index.html consumes it (live organ stats on landing page).

**Trade-off:** disclosure vs visible product surface.

**Status:** Held. The clean fix is "count-only response" instead of 401 — preserves the landing page's live stats without exposing the schema. Implementation: small Caddyfile edit + a count proxy.

## D7. AGI vision thesis — 5 CHRON predictions alignment

The 5 CHRON predictions (D3) appear to be the *formalised* versions of the AGI vision thesis I audited (5 tenses). If so, the calibration fix in D3 is the path to making the thesis *falsifiable* rather than narrative.

**Status:** Held. Recommendation: write a short mapping document `EUREKA-AGI-THESIS-CHRON-MAPPING-2026-10-03.md` next to the 5 CHRON events, so future agents can see which prediction corresponds to which thesis claim.

## D8. F6 EMPATHY vs F6 MARUAH fork (50/50 in your own constitution)

**Originating message:** from earlier 2026-10-03 cross-check. F6 has *three* live variants: F6 EMPATHY (63 hits), F6 MARUAH (69 hits), and a third F6_SOVEREIGN variant.

**Status:** Held. This is a constitutional fork in the federation's own doctrine. arifOS cannot have authority if F6 cannot decide what it is. The choice is Arif's; the agents should not be deciding which F6 to enforce.

**Recommended F13 binary:** "F6 = EMPATHY (Western framing)" vs "F6 = MARUAH (Pacific/Indigenous framing)" vs "F6 = SOVEREIGN (procedural framing)". This is *not* technical; it is *civilizational*. The federation's claimed alignment with arif's cultural / Nusantara substrate (per `agi-nusantara-substrate` skill) suggests MARUAH may be the intended, but EMPATHY is in 63 places.

---

# Summary

| ID | Item | F13 binary | Status |
|---|---|---|---|
| D1 | Reality Engineering / AREP | Resolved ("hold") | Held |
| D2 | Shadow cron chmod | Pending | Queued |
| D3 | CHRON confidence_proposed | Pending | Queued (one-line) |
| D4 | Shadow YAML schema fix | Pending | Queued |
| D5 | Cedar bridge stub | Pending | Queued |
| D6 | /api/organs/* count-only | Pending | Queued |
| D7 | AGI thesis ↔ CHRON mapping | Pending | Optional |
| D8 | F6 fork resolution | Pending | Arif's civilizational choice |

# Closing note

The 2026-10-03 session produced:
- 1 EUREKA synthesis (4 source slices + 8th input cross-check)
- 2 corrections to the base document (narrative completion = normative closure not gap-filling; CoT length is wrong measure)
- 3 phantom citations caught (Anderson 2003, Patt-Zeckhauser 1989, Cogito/Lucy 1986, Lacan pâte, Spurgin review)
- 4 date corrections (Patt-Zeckhauser 2000, Lewis 1979, Kripke 1972/1980, Lehman 1974/1980)
- 1 Caddy edge hardening (verified, /tools.json 401, /health redacted to `{"status":"ok"}`)
- 5 CHRON predictions (registered with calibration defect noted)

The session *also* added 8 deferred items, each with a recommendation. Future agents should treat the EUREKA as the *closed* deliverable and the deferred items as the *open* queue.

**DITEMPA BUKAN DIBERI ⚒️**
