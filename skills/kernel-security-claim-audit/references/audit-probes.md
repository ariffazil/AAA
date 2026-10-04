# Audit probes — copy-paste recipes for kernel security claim verification

All probes are READ-ONLY. No service restart, no key rotation, no secret
printing. Paths + permissions only.

## Probe: "TTL is X seconds" claim

```bash
# Find every TTL constant on arifOS
grep -rn 'TTL_SECONDS\|SESSION_TTL\|DEFAULT_TTL_SECONDS' \
  /root/arifOS/arifosmcp/runtime/ \
  /root/arifOS/arifosmcp/gateway/ 2>/dev/null | grep -v __pycache__

# For each candidate, verify: is it the SCT mint default, the session
# store default, or the WebMCP default?
grep -n 'def mint_sct\|def _get_signing_secret\|def validate_session' \
  /root/arifOS/arifosmcp/runtime/sct.py \
  /root/arifOS/arifosmcp/runtime/session_auth.py
```

**Verdict check:** if you cite a TTL that isn't the file:line of
`mint_sct(ttl=...)`'s default arg, you conflated stores.

## Probe: "Signing key at /path/X" claim

```bash
# Step 1 — read the resolution chain end-to-end
grep -n 'def _get_signing_secret\|_PROD_SIGNING_KEY_PATHS\|_FALLBACK_SECRET' \
  /root/arifOS/arifosmcp/runtime/sct.py

# Step 2 — check live env
echo "ARIFOS_SESSION_SECRET present: $([ -n "$ARIFOS_SESSION_SECRET" ] && echo yes || echo no)"
echo "ARIFOS_SESSION_SECRET_FILE: ${ARIFOS_SESSION_SECRET_FILE:-(unset)}"
echo "ARIFOS_STRICT_MODE: ${ARIFOS_STRICT_MODE:-(unset)}"

# Step 3 — check fallback paths exist (perms only, never read content)
for p in /opt/arifos/app/.signing_key ~/.arifos/signing_key; do
  if [ -f "$p" ]; then
    ls -la "$p" | awk '{print $1, $3, $4, $NF}'
  else
    echo "MISSING: $p"
  fi
done

# Step 4 — confirm strict mode at runtime
curl -s :8088/health | jq '.config.arifos_strict_mode' 2>/dev/null
```

**Verdict check:** if the claim cites one path without listing the full
chain (env → file → paths → fallback), it's an incomplete claim. If the
fallback is `_FALLBACK_SECRET = secrets.token_bytes(32)`, sessions are
unverifiable post-restart in non-strict mode — flag this.

## Probe: "F13 bypass" claim

```bash
# Step 1 — find all Ed25519 verify sites
grep -rn '_pub_key.verify\|verify_init_identity\|verify_sovereign_signature\|Ed25519PublicKey' \
  /root/arifOS/arifosmcp/runtime/ \
  /root/arifOS/arifosmcp/tools/ 2>/dev/null | grep -v __pycache__

# Step 2 — read the canonical 3-stage forge verification
sed -n '800,870p' /root/arifOS/arifosmcp/tools/forge.py

# Step 3 — confirm T3a exempt-actor list (the DESIGNED bootstrap bypass)
grep -n '_ED25519_EXEMPT_SYSTEM_ACTORS' \
  /root/arifOS/arifosmcp/runtime/megaTools/tool_01_init_anchor.py
```

**Verdict check:** "F13 bypass" almost always means either (a) T3a
`_ED25519_EXEMPT_SYSTEM_ACTORS` (designed — NOT a hole), or (b) a
genuinely missing verification gate. Cross-check the actual code path
before declaring a bypass exists.

## Probe: "Gödel lock defined but unverified" claim

```bash
# Step 1 — confirm gate code exists
ls -la /root/arifOS/arifosmcp/runtime/godel_lock_gate.py
ls -la /root/arifOS/tests/constitutional/test_godel_lock_gate.py

# Step 2 — find call sites of the gate (NOT definition = wire-up check)
grep -rn 'godel_lock_gate(' /root/arifOS/arifosmcp/ \
  --include='*.py' 2>/dev/null | grep -v '__pycache__\|godel_lock_gate.py:'

# Step 3 — check self-certifying tools list
sed -n '50,75p' /root/arifOS/arifosmcp/runtime/godel_lock_gate.py

# Step 4 — auditor_validated is advisory or crypto?
grep -n '_auditor_validated\|auditor_validated' \
  /root/arifOS/arifosmcp/runtime/godel_lock_gate.py
```

**Verdict check:**
- Code exists + tests pass → necessary, not sufficient
- `godel_lock_gate(` has callers in pipeline → wired
- `_auditor_validated` reads `params.auditor_validated` string → advisory
  unless cross-checked against signed witness envelope
- New self-cert tool added without editing `SELF_CERTIFYING_TOOLS` →
  silent self-cert path (auditable gap)

## Probe: "self-judge + self-seal" claim

Same as Gödel lock probe. Check `_is_self_certifying()` at
`godel_lock_gate.py:78-101` for caller-vs-target detection. Confirm
arif_judge/arif_seal call paths actually invoke the gate (not just
import the module).

## Probe: "F13 Ed25519 per-call sig required" claim

```bash
# All sig-required gates
grep -rn 'actor_signature\|Ed25519.*verif\|f13_signature' \
  /root/arifOS/arifosmcp/tools/forge.py \
  /root/arifOS/arifosmcp/runtime/cooling_harness.py \
  /root/arifOS/arifosmcp/runtime/darjat_engine.py \
  /root/arifOS/arifosmcp/runtime/envelope_validator.py \
  2>/dev/null | grep -v __pycache__
```

**Verdict check:** each `f13_signature: str = ""` arg is a potential
bypass point. Confirm the call site REQUIRES non-empty string, not
just accepts it.

## Reading the report template

For each claim, output:

- **VERDICT:** CONFIRMED | REFUTED | PARTIALLY-TRUE | NEEDS-F13-RITUAL
- **Severity:** LOW | MODERATE | SEVERE (justify in one line)
- **Evidence:** file:line + ≤3 line excerpt
- **Analysis:** why wrong/right, 2-4 sentences
- **Hardening:** Tier 1 (no F13) | Tier 2 (F13 sign-off) | Tier 3
  (constitutional change) — reversible/irreversible

End with summary table: claim → verdict → severity → key finding.

**Never** print secret values (paths + permissions only). Never restart
services. Never rotate keys.