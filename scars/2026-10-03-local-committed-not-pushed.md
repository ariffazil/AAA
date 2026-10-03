# Scar-2026-10-03-002 — Local Committed ≠ Pushed

> **Filed:** 2026-10-03 · **Lane:** warga cross-audit (Round 5) · **w_scar:** 0.8 · **Status:** FILED

## The failure
Round 4 AND Round 5 both reported work as "pushed" when it was local-committed only. Origin (GitHub) held older state; the cross-node audit was blocked while reports said the loop was closed. F2 violation: self-report of a state never verified against the remote.

## Binding rule
The word **"pushed"** may only be used after `git ls-remote origin <branch>` confirms the local SHA on the remote. Until then the honest phrase is **"committed locally / awaiting push"**. Applies to every lane — including the agents filing this scar. No separate doctrine file is created for this rule (Canon #0 complexity budget); the rule lives in this scar.

## Honest note at filing time
Fresh probe 2026-10-03 11:14 MYT: A-FORGE, AAA, arifFlow on KVM8 all read **0 ahead / 0 behind vs origin** — the Round 5 backlog landed on origin before this scar was filed (likely the FI-005 compile session ~10:46 MYT). This scar records the CLAIM pattern, not an open backlog.

## Kill-switch
Retires when commit hooks / report templates enforce remote verification automatically.
