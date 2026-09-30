---
name: doctrine-to-runtime-compiler
description: "Use when prose doctrine must run as regex + test + receipt."
---

# doctrine-to-runtime-compiler

A class of work that recurs each time a new floor-class doctrine document is ratified: the prose must run, not just exist. This skill is the procedure. The reference holds the table shape and the receipt schema.

## When this skill is the right one

The trigger is the *shape* of the artefact, not its name:

- a markdown / yaml / prose document under `/root/AAA/instructions/`, `/root/AAA/canon/`, `/root/HERMES/`, or `/root/.hermes/SOUL.md` with **prohibition statements** ("don't say X", "never Y", "an instance of X must not bind to Y")
- and the source-of-truth for those prohibitions is **prose** (sentences, tables, lists of forbidden patterns) — not a typed schema
- and a runtime hook exists or can be added where the prohibited output is produced (pre-LLM, pre-tool-call, post-response filter, post-write gate)

If the source is already a typed schema (yaml/json constraint list), skip this skill and go straight to the loader. If the prohibited output has no observable surface, the work is not actionable — report HOLD.

## The four-layer shape every runtime enforcement module needs

| Layer | What it contains | Why |
|---|---|---|
| **pattern tables** | `(name, regex, msg)` tuples, split by consequence: hard HOLD / soft warning / telemetry-only | The hard/soft/telemetry split is the constitutional boundary. Conflating them = system that "fails" everything or "warns" everything — both useless |
| **check function** | `check(text) -> (verdict, reasons)` — the runtime contract | Single entry point; the rest of the system does not need to know which patterns matched |
| **emit functions** | `emit_receipt(reasons, ...)` for HOLD, `emit_drift_telemetry(...)` for telemetry. **Accept `log_path` parameter for test isolation** | Default production path is mandatory; the parameter prevents the test-vs-prod race where the test path is hardcoded |
| **self-test under `if __name__ == "__main__"`** | BM + EN adversarial probes: each expected verdict (ALLOW/HOLD) named explicitly with one-line description | The module is its own integration test; no external harness needed for the smoke check |

**Each layer is independent. A bug in the emit function cannot mask a bug in the patterns. A bug in the self-test cannot mask a bug in check.** That separation is the point.

## The five-step procedure (do not skip or reorder)

1. **Inventory the source.** Count the prohibitions; mark which are HARD (must HOLD) vs SOFT (log only) vs TELEMETRY (observe, never gate). If the source does not distinguish, infer from the wording — "never", "must not", "HARAM" → HARD; "avoid", "prefer not to" → SOFT; "watch for", "drift signal" → TELEMETRY. Record the inference in the receipt.

2. **Extract pattern tables literally.** The patterns in the code must match the wording in the source document. Do not paraphrase. Do not "improve". A reader who audits the code against the source must be able to match each pattern to one sentence.

3. **Write the check + emit functions BEFORE the self-test.** The self-test exists to *prove* check works. If you write the test against a check you haven't built yet, you will iterate against a phantom. **The check must be importable from a separate Python process** — `python3 -c "from runtime.floor_gate import check; ..."` — so the test runs without sharing a kernel.

4. **Adversarial probes go in two passes.** First pass: obvious cases (the prohibition literally stated). Second pass: realistic prose variations — BM Penang register ("hang memang", "kau memang"), reported speech ("X cakap Y"), genuine questions, quoted authoritative text, hedged claims ("maybe but sometimes"). Each pass adds cases that broke the previous pass. Iterate until the pass rate stops climbing — but never claim 100% coverage; record the cases that fail or are ambiguous, they are *known unknowns*, not bugs to hide.

5. **Emit the receipt with two SHA pairs.** (a) the module SHA, before and after the patches the test forced. (b) the test file SHA. The diff between the two module SHAs is the empirical evidence of how much the adversarial probes tightened the patterns — that is the receipt's strongest claim, not the final pass rate.

**Ordering beat:** the self-test runs the module *as a separate process* (`subprocess.run(['python3', module_path])`). If you `import` the module to test it, you lose the production-vs-test isolation that catches the "test path silently bypassed the gate" failure mode.

## Hard rules (each is a lesson, not a procedural nicety)

- **Never promote an SOFT pattern to HARD silently.** If a pattern that started as a warning needs to HOLD, the diff is named ("soft promoted to hard: pattern X — reason Y") in the next receipt, never folded into a routine patch.
- **Never widen a HARD pattern past its source statement.** "Hang is analytical" → HOLD is fine. "Hang is the most analytical" → HOLD is fine. "Analytical" alone → DO NOT add it; the source did not say "the word analytical is forbidden", it said "applying it as a frozen trait to a named person is forbidden". The pattern's scope must match the scope of the source's prohibition.
- **BM Penang acknowledgment tokens are NOT drift.** "OK", "haa", "elok", "bagus" are conversational acknowledgments, not yes-man language. A drift detector that fires on these produces telemetry that lies about its own coverage. English-only first; BM expansion needs a curated negative-list of acknowledgment tokens (separate signal, different shape).
- **Test isolation needs a parameter, not a workaround.** A `log_path` parameter on every emit function is cheaper and more correct than monkey-patching the module's module-level constant. The hardcoded production path stays the default — the parameter is the override.
- **Receipt path is `cache/`, not `tmp/`.** Tmp is for scratch; receipts are durable. They survive the session. If you can't find last session's receipt, the receipt system is broken even when the runtime gate works.
- **A receipt without SHAs is an event pile.** Always record `{pre_sha, post_sha, module_path, test_path, pass_rate, test_exit_code, test_cases_total}`. Without SHAs the receipt is a claim; with them it is evidence.

## Anti-patterns that make the work useless

- **The single-regex module.** One regex with twelve alternatives. Cannot be tested in isolation per pattern. Cannot be soft-promoted independently. Cannot be audited against the source statement-by-statement. Breaks when one alternative needs to be retired.
- **The optimistic self-test.** Cases only where the module is known to pass. Pass rate 100% proves nothing. Adversarial cases that fail are the *signal* the work is honest.
- **The "I read it, it's fine" receipt.** No module SHA, no test SHA, no pass count. A receipt is not a memo. It is a JSON object that another agent can verify against disk.
- **The "drift" pattern that drift-detects everything.** A drift detector that fires on every positive word produces noise that gets ignored. The next genuine drift passes unnoticed because the operator stopped reading. Telemetry that always fires = telemetry that never fires.

## Adjacent skills that stay separate

- `aaa-doctrine-sealing` (governance-ops row 5) — prose → canon prose, **not** prose → runtime code. Different deliverable, different surface test.
- `governance-audit` (governance-ops row 3) — verifies a control is real (caller / effect / bypass proofs). This skill produces a control; the audit verifies one already in place.
- `FORGE-governance-jsonld` — prose → ontology term, for external agents to read. Not for runtime enforcement.

## Output contract

Every invocation of this skill emits:

1. A `runtime/<doctrine>_gate.py` module at the canonical path (or `plugins/<plugin_name>/__init__.py` if the doctrine binds to a specific tool surface)
2. A `tests/test_<doctrine>_gate.py` self-test
3. A `cache/<DOCTRINE>_RECEIPT_<date>.json` with the SHA pair, pass rate, and source-statement-to-pattern map

`F-14` verdict on the work itself: *"adakah manusia lebih dekat kepada reality dan masih memiliki consequence yang lahir daripadanya?"* — yes if the patterns are honest, the test is adversarial, and the receipt is verifiable; no if any of those three is theatre.
