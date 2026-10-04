# Governed Ritual Activation Runbook

> Generalized from the 2026-08-15 AIA activation (sovereign spec → sealed live cron in one session, ~1.5h). Use whenever the sovereign sends a philosophy/spec/ritual design and wants it operating autonomously.

## Preconditions

- Sovereign intent explicit in-session (an order, not a maybe). If ambiguous → the two-door pattern: present judgment + recommendation, let F13 pick.
- Territory check: is it a MODE of an existing agent (preferred) or genuinely a new entity? Functions before entities — modes win.

## Steps

1. **Ground probe (T0).** Verify the substrate the spec assumes actually exists: taxonomy dirs (`ls /root/AAA/arifOS/RESOURCES/`), cadence anchors (e.g. VVV 72h at `/root/memory/VVV/README.md`), related organs' health. Never seal onto imagined structure.
2. **Substrate first (T1).** Write doctrine + policy + workflow files into the RESOURCES taxonomy (04_DOCTRINES / 05_POLICIES / 08_WORKFLOWS), plus any new artifact dirs (with README). Commit with evidence paths in the body. Reversible-first: everything is files/git at this stage.
3. **Phase-split constitutional changes.** Kernel floor table, Holy-8 loop limits, new floors → mark "phase 2 pending", route to a separate 888/F13 session. Do NOT unilaterally amend the constitution.
4. **apex-judge gate before cron.** Build `/tmp/<name>_ev.json` {actor, action, claim, evidence[], scope, reversibility}; run `apex-judge isolate --doer HERMES --candidate "<claim>" -e /tmp/<name>_ev.json --pretty --human`. Quote only: independence_class, effective_verdict, session_id, call_hash. An "authorized" action verdict with HOLD posture (ritual's default) is a GO for infrastructure, not for execution.
5. **Create the cron.** `cronjob action=create`: name kebab-case, `every 72h`-style schedule, deliver=origin, attach_to_session=true, enabled_toolsets minimal (terminal/file/web), prompt embedding the full gate stack + output schema + voice rules (Penang BM, ≤8 lines, no floor numbers, "tiada proposal layak" valid).
6. **Test fire immediately** (`cronjob action=run`) — background; don't poll. Purpose: sovereign sees real output same-day, and gate violations surface now, not in 72h.
7. **Verify on disk, not on report.** When the async result lands: read the receipts the run claims to have written (yaml files, quarantine, blindspots). Re-run sibling-owned test suites to verify THEIR claims (e.g. `forge_aia.py test` → 4/4). Only then report success with commit hashes + paths.
8. **Seal + report.** Activation receipt JSON (cron id, schedule, apex gate fields, F13 directives applied) committed; report in ringgit-aware terms; note the keep-or-kill review date.

## Mid-turn sovereign corrections (out-of-band marker)

Renames, separations, re-scoping arriving mid-turn are applied IMMEDIATELY in the same working turn: `git mv` + doc patches + policy rewrite + cron update in one batch, old dirs left as immutable historical witnesses with README pointers. Do not finish the old plan first.

## Pitfalls

- Cron jobs may fire with the PREVIOUS prompt while you're mid-update (test fire ran pre-demon-gates) — disclose which prompt version a given receipt was produced under.
- Sibling agents work concurrently in `/root/AAA`; uncommitted modified files may be theirs. Check `git log --follow` / authorship before claiming or committing foreign work-in-progress.
- Cron runs must be additive-only (no git commit inside the cron); sealing happens in governed sessions.
- First-run receipts missing newly added fields is expected when the prompt updated after dispatch — the next scheduled run carries the full gate stack.
