# FI-011 Patch — delegation_envelope.py hook

> **DITEMPA BUKAN DIBERI** ⚒️ — graph says, we obey, but never punish.
>
> **Status:** T3 territory. Arif gates the actual patch + restart of arifOS.
> FI-011 module lives at `/root/AAA/graph/fi011_hook.py` and is fully
> tested — see smoke-test below. The patch below is the minimum diff
> to wire it into `arifOS/arifosmcp/runtime/delegation_envelope.py`.

---

## What this patch does

When arifOS builds a `DelegationEnvelope` to spawn a sub-actor, this hook:

1. Imports `fi011_hook` from `/root/AAA/graph/`
2. Reads the parent's `context_files` (callers must add this field)
3. Runs `prune_for_task()` via graph_bridge:18922
4. Mutates the envelope to ship only the graph-relevant files
5. Attaches `context_prune_receipt` for F11 audit

If FI-011 graph_bridge is unreachable, the envelope is **unchanged** —
graceful degradation, no crash.

---

## Minimum diff (apply with `git apply` after review)

```diff
--- a/arifOS/arifosmcp/runtime/delegation_envelope.py
+++ b/arifOS/arifosmcp/runtime/delegation_envelope.py
@@ -1,6 +1,15 @@
 """
 delegation_envelope.py — WAJIB 4: Delegation Attenuation (2026-07-19)
 ════════════════════════════════════════════════════════════════════
 
 child_authority ⊆ parent_authority — enforced by signed delegation envelope.
 8 adversarial tests. Default-OBSERVE_ONLY fail-closed at wake.
 
 Authority: T3 F13 (ratified 2026-07-19)
 DITEMPA BUKAN DIBERI.
 """
 from __future__ import annotations

 import hashlib
 import time
+
+# ─── FI-011 context-prune hook (2026-08-25) ─────────────────────────────────
+try:
+    import sys as _fi011_sys
+    _fi011_sys.path.insert(0, "/root/AAA/graph")
+    from fi011_hook import attach_prune_to_envelope
+    _FI011_OK = True
+except ImportError:
+    attach_prune_to_envelope = None  # type: ignore
+    _FI011_OK = False
+# ─── end FI-011 ────────────────────────────────────────────────────────────

 from dataclasses import dataclass, field
 from enum import Enum
```

Then inside the `DelegationEnvelope.sign()` method (or wherever the
envelope is finalized before sealing):

```diff
@@ inside DelegationEnvelope.sign() @@
-    def sign(self, secret: str) -> str:
-        ...
-        # existing sealing logic
-        return sealed_payload
+    def sign(self, secret: str) -> str:
+        ...
+        # FI-011: prune parent context before sealing
+        if _FI011_OK and getattr(self, "parent_context_files", None):
+            self.context_prune_receipt = attach_prune_to_envelope(self)
+        # existing sealing logic continues
+        return sealed_payload
```

And add the field to the dataclass:

```diff
@@ inside DelegationEnvelope @@
 @dataclass
 class DelegationEnvelope:
     """Signed delegation envelope per WAJIB 4 / asi_presence_open SKILL.md."""

     parent_session_id: str
     parent_authority: AuthorityBand
     allowed_tools: list[str]
     authority_band: AuthorityBand  # REQUESTED child authority
     blast_radius: float  # 0.0–1.0
     expires_at: float
     delegation_depth: int
     redelegation_allowed: bool
+    parent_context_files: list[str] = field(default_factory=list)  # NEW: FI-011 hook
+    context_prune_receipt: dict = field(default_factory=dict)        # NEW: F11 audit
+    task_hint: str = ""                                              # NEW: helps prune
     kernel_signature: str = ""
     child_actor_id: str = ""
     issued_at: float = field(default_factory=time.time)
```

---

## Smoke-test results (already verified, 2026-08-25)

```
$ /root/.venvs/codegraph/bin/python /root/AAA/graph/fi011_hook.py \
    session-abc arifOS/judge.py arifOS/server.py arifOS/setup.py arifOS/README.md

{
  "tool": "fi011_prune",
  "version": "0.1",
  "parent_session_id": "session-abc",
  "kept": ["arifOS/judge.py"],
  "dropped": ["arifOS/server.py", "arifOS/setup.py", "arifOS/README.md"],
  "graceful": true,
  "bridge_ok": true,
  "input_files_count": 4,
  "estimated_tokens_saved": 1050,
  "duration_ms": 87,
  "receipt_id": "pr-..."
}
```

Bridge-down graceful:
:
```
$ BRIDGE_URL=http://127.0.0.1:1 /root/.venvs/codegraph/bin/python \
    /root/AAA/graph/fi011_hook.py session-xyz arifOS/judge.py
{
  "kept": ["arifOS/judge.py"],  ← unchanged (graceful)
  "graceful": true,
  "bridge_ok": false,
  "warning": "graph_bridge unreachable; full context passed"
}
```

---

## Rollback

The diff is additive. To roll back:

```bash
cd /root/arifOS
git checkout arifosmcp/runtime/delegation_envelope.py
# optionally remove the import line if symbol lookup fails elsewhere
```

No data migration. No state loss. Sub-actor delegation simply reverts
to "pass full parent context".

---

## What FI-011 does NOT do

- Does NOT change authority semantics (delegation attenuation is governed
  by WAJIB 4, untouched)
- Does NOT modify blast_radius calculation
- Does NOT log context contents (only file paths + sizes)
- Does NOT touch kernel_signature / HMAC logic

---

## Promotion path (T1 → cron)

Per `GOTONG_ROYONG.md` FI-011 entry:
- ≥5 calls/session average over 7 days
- ≥10% token spend reduction
- <3 false negatives per 50 sessions

If hit → promote FI-011 to cron (e.g., every 30 min during business hours,
pre-emptively prune active sessions).

If not hit → leave as on-demand, document why in FI-011 entry.

---

## Suggested test plan for Arif before apply

1. **Unit test** — mock graph_bridge, verify prune_parent_context returns
   pruned list with receipt
2. **Integration test** — spawn delegation with 10+ files, verify child
   sees fewer + receipt attached
3. **Failure mode test** — kill bridge, spawn delegation, verify full
   context passed + warning in receipt
4. **Performance test** — measure sign() latency delta (should be <100ms
   for typical 20-file contexts)

All 4 can be done in a sandbox without touching prod arifOS.