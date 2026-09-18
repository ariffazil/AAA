# Skill: territory-provenance-assertion

> **Status:** PROPOSED · **Created:** 2026-09-18 · **Forged by:** FI-008 (kimi-code / k3) under PROBE-BEFORE-PANIC (F13-ratified 2026-09-13)
> **Capability, not implementation.** Govern capabilities, not implementations. — APEX-ZEN-CANONICAL-COMPRESSION.md

## 1. Capability contract (binding)

Bounded capability: an AAA agent can assert a territory page's claims carry machine-discoverable MCP-tool provenance by emitting a JSON-LD block that names the `mcp__<organ>__<verb>` tools the page depends on.

## 2. Scope (where this skill binds)

- `/root/arif-fazil.com/sites/arif-fazil.com/dist/**/index.html` (territory dist outputs)
- `/root/arif-fazil.com/forge_work/proposals/*/proposal.md` (proposal-level provenance manifests)

## 3. Out-of-scope (where it does NOT bind)

- Live mutation of `/etc/caddy/Caddyfile` → 888_HOLD, escalate to F13
- Live mutation of `/root/AAA/instructions/*` → 888_HOLD, escalate to F13
- Live mutation of `/root/arif-fazil.com/sites/arif-fazil.com/src/data/**` without rebuilding → requires `make build`, separate gate
- Public write capability exposure → 888_HOLD

## 4. Required MCP tools (this skill depends on)

- `mcp__geox__geox_claim` — for asserting evidence-gated claims
- `mcp__hermes__hermes_claim_validate` — for named-entity claim gate
- `mcp__aforge__forge_fingerprint_check` — for seal-verifier presence
- `mcp__aforge__forge_runtime_verify` — for tool-version checksum
- `mcp__arifFlow__flow_ingest` — for FlowReceipt minting per edit (F11 auditability)

## 5. Workflow (BINDING order)

1. **OBSERVE** — fetch the territory dist page; parse the existing narrative claims
2. **THINK** — map each narrative claim to the MCP tool most likely backing it
3. **CLAIM** — emit a `<script type="application/ld+json">` block with `isBasedOn` array pointing to `mcp__<organ>__<verb>`
4. **VERIFY** — run `make verify-pages`; assert HTTP 200 for modified route
5. **SEAL** — mint a `flow_ingest` step receipt (step_type=Verify, actor_id=af-forge)
6. **WITNESS** — leave audit trail at `/root/AAA/forensics/<territory>-provenance-<date>.json`

## 6. Truth classes (F2 binding)

Every emitted JSON-LD must declare `truthClass` ∈ {`OBS`, `DER`, `INT`, `SPEC`}.

| Claim shape | truthClass |
|---|---|
| Audited IFR arithmetic | OBS |
| Derived metric (composite ratio) | DER |
| Engine interpretation (verdict text) | INT |
| Model parameter (pacemaker threshold) | SPEC |

## 7. Kill-switch (F13 Attention-Kill binding)

```yaml
kill_switch:
  kill_phrase: "STOP territory-provenance-assertion — revert last edit"
  revert_action: "rm <modified_html_file>; git checkout -- <modified_html_file>"
  expected_recovery_time: <60s
  side_effects_on_kill: [none, observability only, no state change]
```

A skill without a kill is decoration. This skill exits cleanly on:
- `make verify-pages` returns non-zero
- existing tripwire score accidentally altered
- any public write capability exposure detected
- Caddy reload attempted

## 8. Reversibility class (F1 binding)

`REVERSIBLE_PRE_HUMAN_DECIDE` — every edit is a static HTML append or stub SKILL.md add. Trivial to revert with `git checkout`.

## 9. F11 Auditability (binding)

Every emit mints a `mcp__arifFlow__flow_ingest` step with `actor_id="af-forge"`, `step_type="Verify"`, `payload.file_path`, `payload.json_ld_hash`. The receipt is sealed into arifFlow's immutable ledger for live auditability.

## 10. F13 Sovereign veto (binding)

Edits affecting `/vitals`, `/000`, `/999`, or any `/etc/caddy/Caddyfile` modification must escalate to F13. This skill **does not grant** authority to seal — only to emit provenance under the precondition that the operator has already approved the territory's payload.

## 11. Operator handoff (F13 silent execution binding)

The skill does NOT call `AskUserQuestion`. It does NOT copy-paste commands to the operator. It:
1. emits JSON-LD provenance edits
2. runs `make verify-pages`
3. mints FlowReceipt
4. reports a tight summary back

If the skill needs a binary decision (architecture · money · irreversible), it 888_HOLDs and reports — it does NOT decide.

## 12. Verification checks before claiming success

- [ ] `python3 /root/arif-fazil.com/scripts/web-zen/web_zen.py doctor` exits 0
- [ ] `make verify-pages` exits 0 for modified routes
- [ ] FlowReceipt minted at `mcp__arifFlow__flow_ingest`
- [ ] No existing claim altered
- [ ] truthClass declared on every JSON-LD
- [ ] isBasedOn array non-empty
- [ ] mcp.arif-fazil.com/mcp endpoint referenced
- [ ] No Caddy reload
- [ ] No public write capability exposure

## 13. Decoration risk (binding per Attention-Kill F13)

If any of the 12 checks above fail, the skill has **decoration risk** and must be patched before re-running. A kill without verification is killing the wrong thing.

---

DITEMPA BUKAN DIBERI · forged, not given.
