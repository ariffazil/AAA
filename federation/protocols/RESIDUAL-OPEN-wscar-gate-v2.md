# RESIDUAL OPEN — W_SCAR gate v2

> **Artefact under description:** `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py`
> **Conformance harness:** `/root/AAA/federation/protocols/test_wscar_gate.py` (11/11 behavioural, 7/7 regex — re-runnable)
> **Recorded:** 2026-09-18
> **Status:** SEALED WITH RESIDUALS — these are known, not overlooked.

## Why this file exists

A prior report claimed this residual list had been written: *"Aku tulis batas ni sendiri dalam
residual_open."* It had not. A search of `/root/AAA` and `/root/.hermes` found `residual_open` only
inside the session database — chat text, never an artefact.

That is the exact failure this gate exists to catch: **a claimed deliverable that exists as
narrative rather than on disk.** The claim was made in good faith about work that was genuinely
done; the note simply never landed. This file closes it.

---

## R1 · Existence is not support  *(the largest residual)*

The gate extracts cited URLs and resolves them. A `200` proves **the citation exists**. It does not
prove the citation **supports the number it is attached to**.

A correct, live URL pasted next to an unrelated figure passes cleanly. Closing this requires
per-claim content matching — fetching the source and checking that the specific value appears in it.
That is a materially larger build than the migration that produced v2.

**Do not describe v2 as "every number is verified".** The accurate claim is: *every consequential
claim now carries a pointer, and that pointer is checked for existence.*

## R2 · `OPS_PATH_WHITELIST` is a genuine bypass

Writes whose target lives under `/root/aaa/`, `/root/arifos/`, `/root/.hermes/`, `/root/forge_work/`,
`/root/agentic/`, `/root/skill-audit/` skip the vocabulary scan entirely.

The rationale is defensible — a write into the doctrine tree addresses no human and therefore owes no
market claim. But it **is** a bypass, and it is load-bearing: this very file, and the harness above,
were written through it. It is receipted as `wscar_ops_exempt` so abuse is countable, not silent.
Removing the exemption is one branch deletion.

## R3 · The gate guards tool payloads, not outbound prose

W_SCAR inspects **tool-call arguments**. It does not inspect the text that actually reaches a human.

Consequence: an unsourced figure typed directly into a chat reply is not caught by this gate at all.
Briefs are protected by the pre-send figure ledger — a **discipline**, not a mechanism. The report
that produced v2 overstated this point. An output-side gate is a different component and does not
exist.

## R4 · No tamper-evidence on the gate itself

The gate file is a plain `-rwxr-xr-x` script with no signature, no self-hash, and no receipt on
write.

**Demonstrated live on 2026-09-18:** the file was rewritten twice within two minutes (08:57:49,
08:59:03) during an active session, and nothing recorded who wrote it. A control that any writer can
redefine silently is a control only for as long as everyone chooses to honour it.

This is R4 because it is the residual with the shortest path to real harm: the gate's authority
derives from the assumption that it is not casually rewritable. **A hash manifest now exists**
(`gate-integrity-manifest.json`) so that future edits become *visible* — but visibility is not
prevention. `chattr +i` would prevent; it was declined because it would freeze a second contributor
mid-work.

## R5 · Two writers, no attribution

The v2 migration and a concurrent contributor both edited the gate and its state within the same
hour. Output was compatible and the contributor's lanes work was an improvement. No attribution
trail exists for either. Mitigated by the integrity manifest; not solved.

## R6 · JITU precedence is asserted, not exercised

JITU is checked before every other rule (line 546, ahead of W_SCAR at 575) and fails **closed** if
its authority module cannot be loaded — correct behaviour. The conformance harness does **not**
exercise this path: tripping the sovereign circuit breaker inside a test would be invasive and could
outlive the test run.

The precedence is therefore verified **statically** (ordering in source), not behaviourally. Treat
`test_wscar_gate.py` as evidence for the W_SCAR path only.

## R7 · Suite scope

The harness covers 11 behavioural cases and 7 regex units. It is a conformance suite, not a proof of
correctness. It says nothing about classification (`classify`), mutation tiers, or the receipt
writer.

---

## Revision duty

Any change to the gate invalidates the manifest hashes. Regenerate with:

```bash
python3 /root/AAA/federation/protocols/test_wscar_gate.py   # must be green first
sha256sum /root/AAA/federation/protocols/arifos-hermes-gate-hook.py
```

and update `gate-integrity-manifest.json`. A manifest that does not match its artefact is worse than
no manifest, because it manufactures trust.

DITEMPA BUKAN DIBERI ⚒️
