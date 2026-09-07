# aaa-governance-fixtures v0.1

Adversarial proof harness — forged 2026-09-07 (FI-008, F13 zen epoch).
Doctrine: **config hygiene ≠ runtime proof.** Binary verdicts, JSONL receipts.

- `run.sh` — executes fixtures F1–F5, F7, F8; emits `results/<ts>.jsonl`
- `fixtures/fake-secret.env` — dummy marker, never a real secret
- `tools.lock.json` — pinned hash manifest of MCP transport surface (mcp.json + launchers + hooks)
- F6 (subagent fork-inheritance) is probed live by the orchestrating agent and appended manually

Semantics declared openly:
- Stop-gate (ANTI-BANGANG) **fails open by design** (loop protection). F3c proves it.
- The future deny-layer **must fail closed**. Its fixtures will demand that.

Red results are not failures of the harness — they are the honest baseline
that the deny-layer mission must turn green.
DITEMPA BUKAN DIBERI.
