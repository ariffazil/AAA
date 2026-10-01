# Temporal Derivation Law — RATIFIED

> **Status:** F13_RATIFIED_SOVEREIGN (2026-10-01 — sovereign token: "SAH SEGALANYA")
> **Provenance:** CHRON phantom-debt incident 2026-09-30/10-01 (one failure class, three instantiations) + sovereign-ratified external *Temporal Reality Architecture* analysis (ChatGPT, external — archived at `/root/AAA/evidence/TEMPORAL-REALITY-ARCHITECTURE-2026-10-01/SOURCE-CHATGPT-2026-10-01.md`). External source was data until F13 ratified its substance; ratification is the sovereign's, not the source's.
> **Companions:** state-transition-discipline.md · recovery-reality-cache.md · authority-envelope.md · apex-reality-kernel (fragment `base`) · CHRON canon

## THE LAW (one sentence)

**Temporal state — what is open, due, overdue, stale — is a query over the causal join, never a stored fact; any surface that materializes it re-derives at read time or carries its derivation instant.**

## Clock separation — never ask one clock to do another's job

Distinct clocks (sovereign-ratified vocabulary): physical · clock · causal · event · observation · knowledge · valid · task · action · authority · human (Kairos) · trajectory.

- UTC wall time → display/audit. Monotonic clock → durations/timeouts. Causal/logical clock (happens-before) → distributed order.
- Never conflated pairs: event time ≠ arrival time ≠ processing time ≠ knowledge time ≠ valid time ≠ transaction time. Timestamps alone never establish which of these a value carries.
- LLM proposes temporal interpretation; runtime enforces temporal consistency. An LLM's "tomorrow" is normalized and verified before execution — never executed raw.

## Clauses

**1 — Join, don't snapshot.** Open/due/active counts derive from birth-store ⋈ verification-ledger at read time (live projection). At federation scale there is no performance justification for materialization. Realized: chron_briefing.py fix + tests/test_briefing_parity.py (2026-10-01).

**2 — One arbiter per object class.** Where multiple surfaces speak about one object class, a designated arbiter is the single winner (e.g. `chron_prediction.get_active()/get_due()`); consumers delegate, never re-derive. Agreement gates become permanent HOLDs; arbitration resolves in one call. Precedent: `duplicate_observation_guard` primary_prediction_id.

**3 — Compare instants, not spellings.** ISO-8601 strings in mixed offset/Z forms are never compared lexicographically. Parse to instant or store fixed-width UTC. (Documented cross-language bug class: SO 20774312, Neo4j #13519, Go RFC3339Nano.)

**4 — Closure must propagate (temporal referential integrity).** `Closure(P) → PropagateClosure(RelatedStates) OR ExplicitException`. When a referent closes, every representation of it closes or records why it remains open. Databases have referential integrity; the federation has its temporal equivalent. Realized precedent: attention-debt phantom-debt guard (d9f4e16).

**5 — WAIT is a first-class action; NOW is a claim.** No agent may infer ACT NOW merely because an action is possible, due, ready, or authorized. Authorized ∧ Ready ∧ Possible ⇏ ActNow. Act now only when value-of-acting-now minus value-of-waiting exceeds cost-of-delay. Repeated control carries minimum dwell / cooldown / observation horizon (epistemic safeguards, not rate limits — Zeno prevention). Unknown human readiness stays UNKNOWN — clock time, calendar-free, or population chronobiology never infer an individual's readiness.

## Non-duplication map (Anti-Bangang LAW 8 — one owner per law)

Of the ratified source's 20 temporal laws, these are ALREADY OWNED elsewhere and are NOT restated here: valid≠transaction (arifFlow RG-PH, bitemporal episodes) · wall-clock≠causal (trace_id receipts, happens-before) · precedence≠causation (causal-attribution discipline, Hermes BIOS) · received-latest≠reality-latest (streaming watermarks, law 1) · due≠ready (P6/attention-debt) · ready≠authorized (authority-envelope) · authorized≠necessary (this fragment, clause 5) · execution-complete≠consequence-known (state-transition-discipline chains) · prediction≠observation (CHRON existence) · repeated-rows≠independent-evidence (duplicate_observation_guard R2) · late-evidence-as-revision (supersession/RETRACTED) · authority-temporal-scope (SCT/ACT TTL, leases) · timeout≠proof-of-failure (SYNCHRONIZATION_FAULT) · irreversible-needs-observation-horizon (BL10 premortem) · human-readiness-not-inferred (WELL consent registry, F6) · temporal-incoherence⇒HOLD (888_HOLD).

## TRUE-AS-OF grammar (mandatory core — two fields)

Every derived temporal surface carries `as_of` (instant of derivation) and `source_head` (last ledger/event position consumed). A consumer whose decision window is newer than `as_of` re-derives or HOLDs. The ratified source's TemporalRealityEnvelope (§15 of archive) is OPTIONAL extension vocabulary per object class — never a mandatory universal schema.

## ΔS discipline

ΔS is an operational/thermodynamic diagnostic — never an ontology of time, never proof of temporal intelligence. **REALITY > CLOCK > MODEL > NARRATIVE — and the clock is only a witness to reality, never reality itself.**

## Research frontier (backlog, not canon)

Computational Kairos · value-of-waiting · temporal credit assignment · multi-agent temporal consensus · temporal uncertainty intervals · counterfactual timing regret · optimal observation horizon · human/machine clock conflict · forgetting vs historical integrity · regime-scoped calibration (REGIME_START/END, CALIBRATION_SCOPE) · causal waiting (sometimes identification requires NOT intervening) · temporal dignity (capability ≠ authority applies to timing). Full list U1–U12: archive §18. Registry: federation work queue, owner CHRON/AAA research lane.

## Machine-checkable seeds

- Falsifier: any surface that stores open/due state AND diverges from the join for more than one derivation cycle.
- Red-team corpus (late/out-of-order/duplicate evidence, clock skew/rollback/DST, authority-expired-mid-task, retry-after-success, completed-but-consequence-unknown, verified-but-event-OPEN, Zeno loops): archive §23 — feed AAA test suite.

DITEMPA BUKAN DIBERI ⚒️
