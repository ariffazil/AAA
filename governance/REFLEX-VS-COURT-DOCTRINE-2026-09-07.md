# Reflex vs Court — Undang-undang Teragih (Distributed Law) · DRAFT

> **Status:** DRAFT_AWAITING_F13 — not canon, not a floor, not self-ratifying.
> **Author:** FI-008 (Kimi Code), 2026-09-07 night session.
> **Commissioned by:** 888 architecture dialogue — *"lajur mana yang layak jadi reflex, lajur mana yang mesti kekal di mahkamah."*
> **Precedent:** Scar Reflex Gate compiled into `A-FORGE/src/interfaces/mcp/shell/forgeShell.ts` (commit `5eb55efe` + `test/scarReflex.test.ts`, uncommitted as of drafting).
> **Related map:** `/root/AAA/governance/ZEN-BIJAKSANA-ARIF-RUNTIME-MAP-2026-09-07.md` (B1, B8, B-tier ordering).

---

## §1 · Principle — Reflex veto, Court authorize

*Reflex boleh menahan; mahkamah yang membenarkan.*

A compiled runtime reflex may return exactly two verdicts: **DENY** or **ESCALATE**. It may never return ALLOW-with-authority. All authority (ACT/SCT, seal, mutation rights) continues to flow only from the kernel court (:8088). This keeps the sovereign's model intact even as law enters the agent body: a spinal arc is not a judge — it flinches, it does not decide.

Consequences:
- Reflex layer is **additive defense**, never a substitute for the court gate. Mutations already require ACT/SCT; if the court is unreachable, mutations fail closed at the court gate regardless of reflex state.
- A reflex DENY is final-at-runtime but appealable (one escalation path to court). A court DENY is final, full stop.
- No runtime code path may mint authority, sign, or seal — F13's Court monopoly is untouched by this doctrine.

## §2 · Eligibility test — five gates, all must pass

A rule may be compiled into a runtime reflex only if:

| Gate | Test | Fail → |
|---|---|---|
| **G-R1 Stability** | Sealed canon, unchanged ≥ 90 days — **or immutable by construction** (scars under F1; these skip the clock) | stays court |
| **G-R2 Determinism** | Decidable by pure local computation: pattern match, fingerprint lookup, schema check. Zero judgment, zero evidence weighing | stays court |
| **G-R3 Locality** | All inputs available at the call site (command text, file path, diff, schema). No cross-organ state, no history lookup beyond a cached table | stays court |
| **G-R4 Fail-closed definable** | Stale data / court unreachable ⇒ DENY mutating ops, allow reads. Never fail-open | stays court |
| **G-R5 Revocation path** | Either immutable (nothing to revoke) or an emergency circuit-breaker exists that degrades to court-only path (never to no-check) | stays court |

One gate failed = the rule stays in the court. No exceptions granted by session momentum.

## §3 · Three-tier law distribution

**Tier 1 — COMPILED REFLEX** (invariant body in runtime, e.g. forgeShell.ts):
- Scar fingerprints *(precedent — wired 2026-09-07)*
- Secret-deny patterns: keys in commands, `.env` in commits, secret material in payloads (ZEN #9)
- Irreversible-syntax deny list: `rm -rf /`-class, force-push to protected refs, `DROP TABLE`-class, firewall mutations, `docker system prune`-class — split into DENY (known-bad) and ESCALATE (ambiguous irreversible)
- Snapshot-before-mutation preconditions (ZEN #4)
- Schema-required-before-write at the tool layer (agent peace)
- Witness-parity log append (mcp-audit.jsonl) — mechanical, append-only

**Tier 2 — REFLEX ENGINE + COURT-HELD TABLES** (stable engine compiled; mutable data cached from kernel with TTL + version + fail-closed revalidation):
- Deprecation registry
- Tool allow/deny data (apex_tool_approval_gate tables)
- Trust-score bands, model allowlists
- Risk-acceptance TTLs (ZEN #18 — expiry needs a clock, the clock's table lives at court)

**Tier 3 — COURT ONLY** (judgment, always):
- arif_judge adjudication, SEAL, musyawarah, W³ tri-witness, P-Dial
- F13 ratifications and every pending gate in the map's Layer ARIF
- Anything tunable by F13 (thresholds: W³ ≥ 0.75, G ≥ 0.80, F13-CS ≥ 0.80)
- Anything under name-dispute (the 11/13 conflicting floor names — map B5)
- Cross-organ consequences, precedent-setting cases, ambiguity of any kind

**The engine-not-table rule:** the unit of embedding is the *engine*, never the *table*. Tables that move live at court and stream outward.

## §4 · Immutability dissolves the trade-off

"Embedded = fast but hard to revoke" is true only for mutable law. Scar constraints are F1-immutable → embedding them costs nothing on the revoke axis; distribution is append-only (new scars flow court→runtime; old scars never retract). The redeploy tax is paid only when an *engine* changes, and engines change rarely by design. Conversely, every F13-tunable knob is maximally expensive to embed — which is exactly why it stays central as data.

## §5 · Promotion & demotion

- **Promotion (court → reflex):** advisory/skill → court-gate (kernel-enforced) → reflex candidate (passes G-R1..R5, ships with a deterministic test — cf. `scarReflex.test.ts`) → compiled. Mirrors gate-promotion ("detection is debt until it can say NO") and RBA shadow→enforce phases.
- **Demotion (reflex → court):** reflex found wrong/over-broad → circuit-breaker flag → degrade to court-only path. Degrade-kill must never leave a no-check path.

## §6 · Sync & lag semantics

The scar store consolidation (map B8) is the distribution channel for Tier-1 data: kernel seals scar → append-only sync to runtimes. Lag on *new* scars is tolerable **only because** the court gate still independently guards mutations — reflex lag is defense-in-depth, never primary enforcement. Tier-2 caches must carry (version, TTL, fetch-fail ⇒ fail-closed for mutating ops).

## §7 · Anti-list — never a reflex

- Musyawarah in-process heuristics (already forbidden to cite as F3)
- Cedar policy *evaluation* until B1 makes the court-side engine real and policies stabilize ≥ 90d — build the court PDP first, distribute engines later
- Biometric/HRV anything — must not exist in any runtime (H-WELL; agents must not invent readings)
- Any rule whose DENY would need judgment to appeal correctly more often than not — if appeals become routine, the rule was never deterministic

## §8 · Shadows / open verification

- ~~Scar Reflex Gate fail semantics unaudited~~ → **AUDITED 2026-09-07 (FI-008), verdict: architecture PASS, matcher DEFECT.** (1) Escalate-only verified in code AND live (ALLOW→GATE only, never authorizes). (2) Missing index → reflex abstains → baseline judge still gates (additive, acceptable). (3) **DEFECT — false-positive matcher:** token match against scar free-prose means `/root` + `forge` path components match "root cause"/"forge-777" in scar text — benign `ls /root/A-FORGE/dist | head` gated with 3 hits. On this VPS nearly every command contains those tokens → reflex degrades to universal friction → 888_HOLD alarm fatigue (vocabulary dilution, anti-bijaksana). Recommended fix: curated `reflex_triggers[]` field on scars (chosen at seal time) instead of prose mining + path-token exclusion + no silent catch. (4) `scarReflex.test.ts` mirrors an OLD matcher (thresholds differ from production) and is absent from `npm test` list. (5) Dry-run returns status "SEAL" alongside judge "gate" — vocabulary inconsistency. Fix (3)+(4) before the A-FORGE dirty commit (map Z7).
- Tier-2 caching does not exist yet — this doctrine describes a target, not a built system.
- 90-day stability clock has no ledger yet; needs a table of canon-stability dates if F13 adopts.
- Naming: "Reflex vs Court" is a working title — Category A name minting is F13's (CANONICAL_GLOSSARY rule).

---

*DITEMPA BUKAN DIBERI — draf menunggu F13.*
