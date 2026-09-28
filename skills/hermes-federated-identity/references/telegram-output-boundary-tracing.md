# Telegram Output Boundary Tracing — Recipe

> When the user reports the wrong register in a lane (menus, closing rituals, header decoder, boot sig, or length cap miss), trace the chain rather than patching what looks wrong.

## The Five-Layer Chain (canonical order)

```
[1] rule      context-governor.md (mode table + hard-ban list)
[2] enforcer  hermes_mcp/_nope_detector.py (regex strip + cap)
[3] gateway   base.py::_thread_metadata_for_source (populates hermes_mode)
              run_turn.py Patch C (populates source.mode BEFORE the metadata builder)
[4] adapter   /tmp/hermes-upstream/.../telegram/adapter.py (calls apply_mode_shape)
[5] classifier hermes_mcp/_conversation_mode.py::classify_mode (decides the mode)
```

Each layer is a candidate. Patch only the layer the evidence names.

## Probe commands (run in order, batch where independent)

```bash
# 1. Rule — is the constraint table intact?
grep -n -A 4 "^│ light" /root/.hermes/lanes/context-governor.md
grep -n "ABCD\|closing ritual\|boot sig" /root/.hermes/lanes/context-governor.md

# 2. Enforcer — are the three regex present and applied?
grep -n -E "(_OPTION_MENU|_DECODER_HEADER|_CLOSING_RITUAL)" \
    /root/.hermes/hermes_mcp/_nope_detector.py
grep -n "_enforce_mode_shape" /root/.hermes/hermes_mcp/_nope_detector.py

# 3. Gateway metadata chain — who populates source.mode?
grep -n -E "source\.mode|setattr.*mode|\.mode =" \
    /usr/local/lib/hermes-agent/gateway/platforms/base.py | head -40
grep -n "classify_mode\|source = dataclasses.replace" \
    /usr/local/lib/hermes-agent/gateway/run_turn.py
grep -n "hermes_mode" /usr/local/lib/hermes-agent/gateway/platforms/base.py

# 4. Adapter — is the enforcer actually invoked and does it REFUSE on IMPORT_FAILED?
grep -n "apply_mode_shape\|IMPORT_FAILED" \
    /tmp/hermes-upstream/plugins/platforms/telegram/adapter.py

# 5. Classifier — last, not first
grep -n "def classify_mode\|return ModeVerdict" \
    /root/.hermes/hermes_mcp/_conversation_mode.py
```

## Verification, not green-light

When the user proposes a diagnosis, verify before agreeing. The chain has been patched at multiple scars; stale hypotheses from earlier sessions still circulate. The honest move is:

- run the grep that disproves the hypothesis first if you suspect it,
- if the hypothesis holds, run the grep that confirms it,
- if both probes return evidence, present both, not one.

A diagnosis that the code doesn't support is a hallucinated root cause — patching it ships the same leak with a different label.

## Common mis-reads to watch for

- `DEFAULT_MODE` in `_send_boundary.py` is `"light"` (240 char cap), NOT `"analyst"` (1800 char). Older transcripts and patch comments that cite `DEFAULT_MODE = "analyst"` are stale. Always grep `^DEFAULT_MODE =` on the live file.
- The metadata chain has TWO populate sites: `run_turn.py` sets `source.mode`, then `base.py::_thread_metadata_for_source` copies it to `metadata["hermes_mode"]`. If you grep only `base.py`, you find no `source.mode =` assignments — that absence is correct, not a bug.
- Two enforcers coexist: `_nope_detector._enforce_mode_shape` and `_send_boundary.apply_mode_shape`. The adapter calls `apply_mode_shape`. `_nope_detector` is invoked from the classifier/runtime. Distinguish which one fires on outbound before patching.
- The adapter's opt-out gate is `metadata["hermes_mode"] == "bypass"`. If the user complaint includes "I set mode manually and it still leaked", check the bypass path before the cap.

## Patch flow (after the leak is identified)

1. Make the smallest change that closes the specific gap — never bundle unrelated cleanup.
2. Verify with a fresh probe on the patched layer.
3. Surface the change to the user with: layer patched · change made · verification grep result.
4. Do NOT restart the gateway from inside the running gateway process (SIGTERM propagates) — see the gateway-restart pitfall in SKILL.md §3.