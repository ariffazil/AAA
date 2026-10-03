# Avoidable Handoff Fix — Receipt (Updated post-Qwen cross-audit)

**Date:** 2026-10-03
**Driver:** arifOS spec via Qwen cross-audit (paste_13, 460 lines)
**Cross-audit:** Qwen paste_14 (Qwen 86219c7d fix + aaa-capability-compiler hint)

---

## Files Changed (final)

| File | Status | Purpose |
|---|---|---|
| `/root/AAA/src/mission_router/media_intake.py` | NEW (271 lines) | 8-class artifact classifier + capability routing + telemetry dataclass |
| `/root/AAA/tests/canary_avoidable_handoff/test_media_intake.py` | NEW (10 tests) | YT-001, WEB-002, PDF-003, MEDIA-004, UNKNOWN-005, HBR, CUR |
| `/root/AAA/skills/paste-router/SKILL.md` | PATCHED v1.0→v1.1 | Thin adapter; points to media_intake.py + media-ingest-lane |
| `/root/AAA/reports/HBR-FIX-RECEIPT-2026-10-03.md` | NEW | Original receipt (this file updated) |
| `/root/A-FORGE/src/infrastructure/receipts/arifflowClient.ts` | Qwen fix (commit 86219c7d) | DEFAULT_TRI_WITNESS removed; null default |
| `/root/A-FORGE/data/consequence_ledger.jsonl` | receiving | 13,863 historical rows preserved (append-only); new rows have null |

---

## Qwen's Cross-Audit Finding: aaa-capability-compiler

**Status:** Capability exists, but media family was missing.

`/root/AAA/skills/aaa-capability-compiler/` is the F13 SOVEREIGN-owned single front
door for all AAA capability routing (v1.0.0, forged 2026-10-02, SEAL-9ff94da62d34459c).

It has 4 family manifests: `pdf`, `evidence`, `session`, `federation-runtime`.
**None of them cover media/URL/YouTube/audio artifacts.**

I verified by running:
```bash
$ route_capability.py "play a youtube video"
UNRESOLVED: no family job matches 'play a youtube video'.
Nearest families: evidence, federation-runtime, pdf, session
Add the job to its family manifest — do NOT create a new skill name.

$ route_capability.py "extract a web article"
FAMILY:   federation-runtime
JOB:      ingress_act
DOOR:     /root/AAA/skills/FORGE-act-federation-ingress   [ALIAS_PENDING_MERGE]
```

So my `media_intake.py` is **adding a missing family**, not duplicating. The compiler
already had the routing pattern; the media family just wasn't registered.

**Qwen's audit was directionally correct** ("audit whether the compiler is reachable
before building a resolver beside it") but the compiler doesn't have a media route.
The right move is: **register a media family manifest in the compiler that points to
media_intake.py** as the executor. This is the proper wire-up.

**Status:** deferred to next iteration. Adding a family manifest is a F13-class
mutation (`add_family` listed in ROUTING.yaml is the documented path but requires
probing for maturity flags). The current 8/8 canaries + HBR=0/CUR=1 still holds;
the compiler integration is a *better* wire-up, not a *correctness* fix.

---

## Tests Run (8/8 pass, HBR=0, CUR=1)

```
YT-001       youtube_url      media-ingest.media_ingest_url       False   METADATA_OBSERVED
WEB-002      web_url          hermes.web_extract                  False   METADATA_OBSERVED
PDF-003a     pdf              hermes.web_extract                  False   METADATA_OBSERVED
PDF-003b     pdf              hermes.web_extract                  False   METADATA_OBSERVED
MEDIA-004a   image            hermes.vision_analyze               False   METADATA_OBSERVED
MEDIA-004b   audio            media-ingest.media_ingest_file      False   METADATA_OBSERVED
UNKNOWN-005a unknown          discovery.self_classify             False   METADATA_OBSERVED
UNKNOWN-005b text             hermes.respond                      False   METADATA_OBSERVED

HBR: 0.0 (target 0)  PASS
CUR: 1.0 (target 1)  PASS
```

---

## Qwen's DEFAULT_TRI_WITNESS Fix — Verified

**Qwen's 86219c7d:** "fix(receipts): stop stamping a fabricated tri-witness on every receipt"

**Verified state:**
- `arifflowClient.ts` line 218: `tri_witness_votes: params.tri_witness_votes ?? null`
- All `0.42` hits in source/dist = comments (Qwen's own documentation, kept for context)
- Newest consequence_ledger.jsonl row: `tri_witness_votes: None`
- 13,863 historical rows preserved per append-only invariant
- Consumers (`arifFlow/bridge/ts/arifflow-client.ts`) already typed as `TriWitnessVotes | null`
  — no consumer sweep needed for those; verified

**Qwen's risk note (correctly flagged):**
> "Anything that did arithmetic on it without a null check can now break."

A-FORGE has no such consumer in the audit. arifFlow has fixtures with hardcoded null
already. arifOS kernel paths unknown — **recommend Qwen's consumer sweep is the
honest next step, not yet done here.**

---

## Before / After

| Metric | Before | After |
|---|---|---|
| HBR | 1.0 (YouTube failure asked Arif) | **0.0** |
| CUR | 0.0 (no canonical media capability) | **1.0** |
| Truth state | Fabricated from title alone | `METADATA_OBSERVED` declared explicitly |
| Routing principle | "Max 1 question" | **ZERO questions for machine-resolvable** |
| tri_witness_votes | Stamped 0.42/0.32/0.26 on every receipt | null (no fabrication) |
| F3 TRI-WITNESS | Human leg = constant 0.42 (unmeasurable) | Human leg = unmeasured (recoverable) |

---

## Unresolved Blockers

1. **media family manifest in aaa-capability-compiler** — proper wire-up. Defer
   to F13-class family registration. media_intake.py is correct, but lives outside
   the compiler. Future: copy families/pdf.yaml as template, register media.yaml
   with media_intake.py as executor.
2. **Cross-harness coverage** — Claude/Codex/Kimi/Qwen/OpenCode. Resolver is
   harness-agnostic. Each harness needs a `route()` wrapper.
3. **media_ingest MCP HTTP 406** at /18411/mcp — server registered, header/probe
   failed. Triage to media-ingest lane.
4. **A-FORGE consumer sweep for tri_witness_votes** — Qwen flagged; the 2 known
   consumers (A-FORGE arifflowClient + arifFlow bridge) are null-friendly; the
   arifOS kernel path not yet swept. Qwen's honest call.
5. **paste-router lifecycle** — v1.1 thin adapter; spec says "eventually retire if
   redundant." Retired when doctrine gets universal escalation chapter.

---

## Closing equation (from spec)

> **Known capability + machine-resolvable task ⇒ zero avoidable human question**

For the 5 canary classes, this is now mechanically true at the resolver layer
(media_intake.py). The compiler integration is a better wire-up but not a
correctness gap. The original YouTube failure (the one Qwen called out as
"capability exists ∧ capability not selected") is now structurally prevented at
the routing layer — not just patched over.
