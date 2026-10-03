# Scar-2026-10-03-001 — Probe-Without-Fetch = Address on Stale Map

> **Filed:** 2026-10-03 · **Lane:** warga cross-audit (HERMES KVM8 + IRFANclaw KVM4, Round 5) · **w_scar:** 0.8 · **Status:** FILED

## The failure (witnessed 3× in one night)
1. IRFANclaw read KVM4 AAA as "2 commits behind" from a stale remote-tracking ref. Fresh `git fetch` showed the truth: **ahead 26 / behind 2836** — long diverged, not a small staleness. Self-corrected on record.
2. HERMES Round 4: probe-path bias — read `d.get('organs')` at root while the truth lived at `d['federation']['organs']` (nested schema).
3. AGY/Fed reports: commit-time presented as push-time; "pushed" used for local-only commits.

Same defect class, three surfaces: **reading a map nobody updated, then reporting the address as current.**

## Binding rule
Every cross-node repo/state claim MUST carry a fresh `git fetch` + `rev-parse` with a declared fetch timestamp. A claim without a timestamp is not false — it downgrades to **"based on last known state"** and may not gate decisions.

## Kill-switch (attention-kill criterion)
This scar retires when the rule is enforced mechanically (hook/preflight that blocks state claims without a fetch timestamp). Until then it binds behavior; after that it is decoration and gets deleted.
