# Reality Binding Architecture — Authority → Physics

> **Status:** DRAFT — pending F13 ratification
> **Date:** 2026-09-17
> **Origin:** Federation-wide audit (audit 2 of 10 services correctly bound to OS users; VAULT999 ledger files 644/world-readable)
> **Companion:** APEX-ZEN-CANONICAL-COMPRESSION.md · AUTHORITY-ENVELOPE.md · FI_DRIFT_GOVERNANCE.md
> **Motto:** DITEMPA BUKAN DIBERI ⚒️

---

## 0. Compression

```text
Policy says X.
Physics says Y.
Physics wins. Always.

A constitutional architecture is only complete
when authority is encoded into physics.
```

---

## 1. The Pattern (Repeatedly Observed)

Across audits:

```text
User exists       ≠  Service uses user      (geox user exists, geox-mcp runs as root)
Group exists      ≠  Permission bound        (forge group empty, a-forge-mcp runs as root)
Policy exists     ≠  OS enforces policy      (arifOS says "no root", aaa-a2a in ariffazil group)
Ledger exists     ≠  Ledger protected        (VAULT999 dir 750, but jsonl files 644 world-readable)
Agent exists      ≠  Agent constrained       (FRAME is "OBSERVE_ONLY" but frame-mcp runs as root)
```

**This is not a fix-list. It is an architectural shape.**

Every governance gap maps to an OS physics gap.
The fix is not `chmod 600`. The fix is **Reality Binding**.

---

## 2. The Metric: Binding Ratio

```text
                    authorities physically bound to OS physics
Binding Ratio  =  ─────────────────────────────────────────────────
                      authorities declared in governance layer
```

### Example (current federation):

```text
Governance authorities declared:  10
  - arifOS      → JUDGE_ONLY
  - A-FORGE     → EXECUTE_AFTER_SEAL
  - GEOX        → COMPUTE_ONLY
  - WEALTH      → EVIDENCE_ONLY
  - WELL        → REFLECT_ONLY
  - FRAME       → OBSERVE_ONLY
  - arifFlow    → METABOLISM_ONLY
  - HERMES      → RELAY_ONLY
  - AAA         → COCKPIT_ONLY
  - VAULT999    → WITNESS_ONLY

Authorities physically bound:       2
  - arifOS service    → User=arifos     ✅
  - WEALTH service    → User=wealth     ✅

Binding Ratio = 20%
```

### Target:

```text
Binding Ratio → 100%
```

Every declared authority has a corresponding OS-level enforcement:
- UID/GID for service identity
- File permissions for storage boundaries
- Network namespace for reachability
- Capability drops for privilege reduction
- `ProtectSystem` / `ProtectHome` for filesystem containment
- `chattr +i` / `chattr +a` for immutability

---

## 3. The Five Layers (Bottom-Up Binding Required)

```text
Layer 5  Reasoning       (LLM output)
Layer 4  Prompt          (system prompt, few-shot)
Layer 3  Contract        (API schema, capability envelope)
Layer 2  Code            (application logic)
Layer 1  Process         (PID, UID, namespace)
Layer 0  Physics         (Linux kernel: permissions, capabilities, cgroups)
```

**The Binding Ratio measures: how many declared authorities at Layer 3-5 reach Layer 0.**

If a contract says "GEOX cannot mutate VAULT999", but GEOX runs as root, the authority exists at Layer 3 but not at Layer 0. **The gap is the failure mode.**

---

## 4. The Law

```text
PHYSICS > POLICY > PROMPT > INTENTION
```

Reading down: a more physical layer always overrides a less physical layer.
- A `chmod 600` overrides a README that says "private"
- A `User=geox` overrides a prompt that says "GEOX shall not..."
- A capability drop overrides a capability declaration

**If you want authority to be real, it must be physics.**

---

## 5. Reality Binding as a FRAME Signal

The Binding Ratio should not be a one-time measurement. It should be a **FRAME drift check**.

### FRAME Chamber 7 (new): reality_binding

```text
For each organ in organs.yaml:
  1. Read declared authority_ceiling (Layer 3)
  2. Read systemd unit User= directive (Layer 1)
  3. Read effective UID from running process (Layer 0)
  4. Compute: declared_authority ↔ effective_uid match?
  5. Check: vault file permissions match declared access?
  6. Output: binding_ratio per organ + aggregate
```

### Output schema:

```json
{
  "binding_ratio": {
    "total_declared": 10,
    "total_bound": 2,
    "ratio": 0.20,
    "per_organ": {
      "arifOS":    {"declared": "JUDGE_ONLY",       "uid": 994, "bound": true},
      "a-forge":   {"declared": "EXECUTE_AFTER_SEAL", "uid": 0,   "bound": false},
      "geox":      {"declared": "COMPUTE_ONLY",     "uid": 0,   "bound": false},
      "frame":     {"declared": "OBSERVE_ONLY",     "uid": 0,   "bound": false},
      ...
    },
    "vault_protection": {
      "directory": {"perm": "750", "owner": "ariffazil", "bound": true},
      "ledger_files": [{"path": "...", "perm": "644", "world_readable": true, "risk": "HIGH"}]
    }
  },
  "overall_verdict": "PHYSICS_GAP",
  "delta_from_last": "+0%"
}
```

This makes Binding Ratio **observable**, not just aspirational.

---

## 6. The Minimum Viable Binding (per organ)

For each organ, the minimum OS-level enforcement to match its declared authority:

| Authority | OS Minimum |
|-----------|-----------|
| JUDGE_ONLY | Dedicated UID. `ProtectHome=read-only`. No network bind except 127.0.0.1. `CapabilityBoundingSet=` minimal. |
| EXECUTE_AFTER_SEAL | Dedicated UID. Write access ONLY to A-FORGE workspace. No direct VAULT access without SEAL token. |
| COMPUTE_ONLY | Dedicated UID. Read-only on its data dir. No write to any /root/* path. |
| EVIDENCE_ONLY | Dedicated UID. Append-only on its ledger. `chattr +a` on output files. |
| REFLECT_ONLY | Dedicated UID. No external network. Read-only on state.json. |
| OBSERVE_ONLY | Dedicated UID. No write to ANY organ data dir. Read-only everywhere. `ProtectSystem=strict`. |
| METABOLISM_ONLY | Dedicated UID. Write to arifFlow receipts only. Append-only. |
| RELAY_ONLY | Dedicated UID. No file write. Network proxy only. |

---

## 7. The Operational Law

```text
Before declaring any authority:
  → What OS-level mechanism will enforce it?
  → What UID/GID will own it?
  → What file permissions contain it?
  → What capability drop limits it?
  → What immutable flag protects it?

If the answer is "we'll add it later":
  → The authority is NOT declared. It is wished for.
```

---

## 8. Status

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Pattern recognition (Binding Ratio) | ✅ DONE 2026-09-17 |
| 1 | FRAME Chamber 7: reality_binding | PENDING |
| 2 | Per-organ minimum viable binding | PENDING |
| 3 | Execute minimal fix (one organ at a time, reversible) | PENDING |
| 4 | Track Binding Ratio over time | PENDING |

---

## 9. Final Compression

```text
EUREKA-1:  Files don't create reality. Execution paths create reality.

EUREKA-2:  Authority doesn't create reality. Binding creates reality.

EUREKA-3:  A constitutional architecture is only complete
            when authority is encoded into physics.
```

The user accounts, groups, ACLs, `chattr`, systemd `User=`, containers, and permissions are not "ops work".

They are the machinery for turning:

```text
Intent  →  Machine Reality
```

---

## 10. Baseline Measurement (2026-09-17)

```text
BINDING RATIO: 57% (4 bound / 3 unbound / 3 not running)
VERDICT: PARTIALLY_BOUND
```

| Organ | Declared | Running As | Status |
|-------|----------|------------|--------|
| arifos | JUDGE_ONLY | arifos | ✅ BOUND |
| a-forge | EXECUTE_AFTER_SEAL | root, forge | ✅ BOUND |
| geox | COMPUTE_ONLY | root | ❌ UNBOUND |
| wealth | EVIDENCE_ONLY | wealth | ✅ BOUND |
| well | REFLECT_ONLY | (not running) | ⚠️ INACTIVE |
| frame | OBSERVE_ONLY | frame | ✅ BOUND |
| arifflow | METABOLISM_ONLY | root | ❌ UNBOUND |
| hermes | RELAY_ONLY | (not running) | ⚠️ INACTIVE |
| aaa | COCKPIT_ONLY | aaa-a2a, aaa-preforge | ❌ UNBOUND |
| vault999 | WITNESS_ONLY | (not running) | ⚠️ INACTIVE |

**VAULT999 ledger files: 82 are world-readable (644)** — chain integrity files exposed.

---

## 11. Case Study: GEOX Binding Attempt (2026-09-17)

**Attempted:** Bind GEOX to `geox:geox` user (already exists, UID 983).

**Result:** Service failed to start. Reverted to `root` (operational recovery).

**Root cause:** `/opt/geox/.venv` was installed by root with restrictive ACLs:
```text
owner: root
group: root
group::---        ← no group access
other::---        ← no other access
```

When systemd tried `ExecStart=/opt/geox/.venv/bin/python3 ...` as user `geox`, the kernel denied traversal of `/opt/geox/.venv`.

**Deeper discovery (Linus insight):** The data layout was designed assuming root access. Binding authority to physics requires also fixing the data layout. The act of binding **reveals all the hidden root-assumption dependencies**.

**The fix requires (not executed — larger sprint):**
1. Reinstall GEOX venv as `geox:geox` user
2. Move `/opt/geox/data` and other write paths outside `/root/`
3. Or: set up ACL grants for geox user on `/opt/geox/.venv` recursively
4. Or: containerize GEOX (namespaces are the kernel-level binding)

**This is the natural next step:** The Binding Ratio cannot be increased without a data migration plan. Each binding attempt that fails teaches us exactly what migration is needed.

---

## 12. FRAME: Proof of Concept (Already Bound)

FRAME was already correctly configured at install time:
```text
User=frame, Group=frame
ProtectSystem=strict
ProtectHome=read-only
ReadOnlyPaths=/root/AAA/federation/frame
ReadWritePaths=/opt/frame/app
```

**Result:** Frame runs as UID 978, completely isolated from root paths it doesn't need. This is what every organ should look like. FRAME is the template for future bindings.

**Key takeaway:** FRAME was bound because it was installed with binding in mind. The other organs weren't. Retroactive binding is harder but possible — GEOX is the next candidate, with a data migration plan.

---

## 13. Operating Principle

```text
The Binding Ratio is a leading indicator of architectural integrity.

It rises when:
  - Services are installed with dedicated users
  - Data layouts avoid /root/ paths
  - Permissions match declared authorities
  - Containers/namespaces replace filesystem ACLs

It falls when:
  - New services default to root
  - Data accumulates in /root/
  - ACLs are added without audit
  - "Just run as root" becomes the default
```

**Every new service should be born with a non-root User= directive.**
**Every new data path should avoid /root/ if a non-root user will need it.**
**Every existing binding attempt reveals the migration cost — and the migration cost is the price of the original shortcut.**

---

*DITEMPA BUKAN DIBERI ⚒️*
*The pattern is the medicine. The chmod is the prescription.*
*The diagnosis IS the discovery.*
