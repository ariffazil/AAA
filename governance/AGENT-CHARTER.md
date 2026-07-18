# Agent Working Charter — arifOS Federation · draft v0.1

> Drafted 2026-07-18 by kimi-code (FI-008) for Muhammad Arif bin Fazil (F13 SOVEREIGN).
> Review pending. This is an additive delta; `/root/AGENTS.md` remains authoritative.

## Prime invariant

> Lower the entropy for the next agent.

Leave fewer contradictions, fewer duplicate sources, a smaller decision surface, and one verified next step. If an artefact does not make the next agent's work simpler, more truthful, or more reversible, do not add it.

## Working rules

1. Read live state before acting: `git status`, runtime health, ports, then Observatory. A snapshot is evidence for its observation time, not permanent truth.
2. Keep the public eight-tool wire unchanged while draining internal duplication.
3. One commit tells one story and has one-step `git revert` rollback.
4. Before deletion, use `rg` to prove zero imports, symbol consumers, service entrypoints, and tests. A filename-only search is insufficient.
5. If another actor changes a file, surface and classify it. Never hide, silently fold, overwrite, or discard it.
6. Observatory is a witness, not authority. Verify both findings and green states with direct probes.
7. Unknown stays unknown. Never convert missing measurement into green.
8. No commit is done without a falsifiable test; no deploy is done without post-deploy health and provenance proof.

## Re-runnable phase gate

From `/root/arifOS`:

```bash
python3 scripts/sync_kernel_abi.py --check
PYTHONPATH=. python3 -c 'from arifosmcp.kernel.substrate_readiness import assess_substrate_readiness as a; r=a(); print(r.to_json()); raise SystemExit(r.overall_verdict != "PASS")'
python3 scripts/pin-surface-map.py --ci --require-live-mcp
PYTHONPATH=. python3 -m arifosmcp.transport.conformance_spine
```

Then verify Observatory's seven states individually and compare `/root/arifOS` HEAD plus dirty state against the deployed commit. A working-tree mismatch keeps F-008 OPEN.

## Stop boundary

Stop for irreversible operations, constitutional changes, secret rotation/exposure, public communication, force-push to main, Caddy/VPS restart, VAULT mutation, or production deploy without green gates. Routine reversible source work continues with receipts.

## Handover shape

End work with only four facts:

- outcome;
- changed files or commit hashes;
- gates run and honest failures;
- one next safe action.

Canonical location: `/root/AAA/governance/AGENT-CHARTER.md`. Original draft v0.1 retained at `/root/forge_work/2026-07-18/AGENT-CHARTER-V0-2026-07-18.md` for audit trail. Promoted by sovereign (888) on 2026-07-18.

DITEMPA BUKAN DIBERI — forged, not given.
