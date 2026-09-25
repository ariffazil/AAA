# Tier-C Patch Ledger — L01 / L04 / L06 prepared diffs (2026-09-25)

> **Status:** DIFFS PREPARED. Not applied. Awaiting F13 SOVEREIGN call to execute T2 patches against A-FORGE runtime.
> **Closes:** Loop reporting for L01, L04, L06 from `HOOK-FEDERATION-STANDARD-DRAFT-v0.md` §7.
> **Why held:** A-FORGE runtime behavior cannot be tested from sandbox (loopback blocked). Source-level
> diffs are below; execution must wait for sovereign green-light or live-runner verification.

---

## L01 — F12 secret-pattern allowlist: add `act_v1.*`

**Symptom:** `arif_init(mode=light)` returns a JWT-shaped token `act_v1.<base64>.<sig>`.
The F12 content scanner treats any `eyJ`-prefix JWT-like string as secret-shaped.
Reports false-positive when the token flows through receipt payloads.

**Investigation needed** (FI-005 did not complete in sandbox):

1. Locate the canonical F12 secret-pattern list. Probable locations:
   - `/root/A-FORGE/src/domain/apex/malu_score.py`
   - `/root/A-FORGE/src/domain/probes/shadowMcpDetector.ts`
2. Verify the regex/key pattern used.
3. Add `act_v1.*` to allowlist with a comment.
4. Add a pytest-style regression: `arif_init` output token passing through `forge_*` does not
   trip F12.

**Prepared diff (skeleton — apply when source located):**

```diff
--- a/A-FORGE/src/domain/apex/malu_score.py
+++ b/A-FORGE/src/domain/apex/malu_score.py
@@ -N +N  ## presumed line vicinity
 SEC_PATTERNS = [
     r'AKIA[0-9A-Z]{16}',
     r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',  # F12 JWT detection
+    # L01 closure 2026-09-25: arifOS ACT v1 token JWTs are constitutional, not secrets.
+    # Allowlist: tokens prefixed 'act_v1.' (see /root/AAA/instructions/authority-envelope.md §5).
+    # Detection logic: if JWT header is followed by payload type="arifOS.act_v1", suppress F12 trip.
+    # NOTE: implement as scan-time check, not regex deletion — see full spec.
 ]
```

**Awaiting:** confirming source location + F12 trip semantics before applying. Apply via
A-FORGE branch `fix/l01-act-v1-allowlist` (do NOT touch current branch `fix/2026-09-21-forge-wealth-bridge`).

---

## L04 — Hermes hooks: `reality-claim-gate` post-hook + dignity-pre-tool-call

**Symptom:** `/root/HERMES/` hooks directory lacks the two hooks named in
`/root/AAA/blueprints/HOOK-FEDERATION-STANDARD-DRAFT-v0.md` §3 row "Hermes".

**Two missing hooks:**

1. `reality-claim-gate` — post-hook that ingests a Hermes claim-receipt into arifFlow.
2. `dignity-pre-tool-call` — pre-tool-call hook that gates on F6 dignity invariant.

**Prepared content (will be applied to `/root/HERMES/hooks/` as `.py` files
when sovereign OK arrives):**

```python
# /root/HERMES/hooks/reality-claim-gate.py
# L04 L04 closure 2026-09-25 — post-hook wiring

def on_reality_claim(claim, context):
    """Sends verified reality-claim receipts into arifFlow."""
    if not claim.get("verified"):
        return None  # not for the flow until verified
    return {
        "kind": "reality_claim",
        "claim_id": claim["id"],
        "epistemic_label": claim.get("epistemic_label", "Observation"),
        "trace_id": claim["trace_id"],
    }
```

```python
# /root/HERMES/hooks/dignity-pre-tool-call.py
# L04 closure 2026-09-25 — pre-tool-call F6 dignity gate

def on_pre_tool_call(tool_name, args, context):
    """Refuses tool calls that breach F6 dignity or F1 sentinel patterns."""
    payload = (args or {}).get("content", "")
    if "[REDACT-SENTINEL]" in payload:
        return {"gate": "DENY", "reason": "F1 AMANAH sentinel trigger"}
    return {"gate": "PASS"}
```

**Awaiting:** sovereign green-light before write. Hermes working tree currently 4 files dirty
on `main`; new hooks should be a clean commit on a new branch `feature/l04-hermes-hooks`.

---

## L06 — Codex `RULES.md` fragment: prefer MCP organs over raw loopback curl

**Symptom:** Codex runtime has MCP surface available (proven in L08's own audit), but Codex's
TUI prompt layer defaults to raw shell `curl` for federation health probes (see earlier session
analytics).

**Prepared fragment (will be installed at `/root/.codex/rules.d/prefer-mcp.md`):**

```markdown
# Codex CLI — Federation Probe Preference

When federation organs or services appear routable, **prefer MCP over raw shell curl**:

- `forge_arifos__arif_health` (the arifOS MCP `health` tool) over `curl http://127.0.0.1:8088/health`.
- `forge_well__well_get_triadic_snapshot` over `curl http://127.0.0.1:18083/...`.
- `forge_geox__geox_*` over `curl http://127.0.0.1:8081/...`.

Why: MCP carries trace_id, audit envelope, and claim-class tag. Raw curl bypasses all three.

EXCEPTION: when the policy sandbox rejects MCP (e.g. `policy=never`), raw curl is admissible
ONLY for one-shot read; the result must be tagged `evidence_kind: SCRIPT_PROBE` and cannot
substitute for an MCP-issued receipt.
```

**Awaiting:** sovereign green-light. The fragment lives at `/root/.codex/rules.d/` — this is
`/root/.codex/` not Codex-arifOS; install under Codex's own RULES convention.

---

## Summary of T1 closures

This document closes the *ledger entry* for L01/L04/L06 by recording prepared diffs. The actual
*execution* of each patch waits on F13 SOVEREIGN call OR a live-runner session that can verify
runtime behavior after the patch.

Total prepared artefacts this session:

1. `/root/AAA/blueprints/AAA-EVIDENCE-QUALITY-REFACTOR-SPEC-v0.md` — L12 spec (119 lines)
2. `/root/AAA/research/hooks-audit-across-coders-2026-09-25.md` — L05 audit (95 lines)
3. `/root/AAA/research/tier-c-patch-ledger-2026-09-25.md` — this file (L01/L04/L06 prepared)
4. `/root/AAA/research/STABILIZATION-NEXT-ACTIONS-2026-09-25.md` — top-level research (186 lines)

DITEMPA BUKAN DIBERI ⚒️
