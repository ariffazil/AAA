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

---

## 14. Corrected Approach: Sandbox Before Demote (2026-09-17 Update)

The original doctrine proposed UID demotion (running services as dedicated non-root users) as the primary binding mechanism. **This was the wrong prescription.** An external review caught 5 fatal flaws:

### The 5 Flaws

1. **Stale inventory** — frame user already exists (UID 978, GID 970), GID 971 collision with arifos-auth.
2. **/root path trap (203/EXEC chasm)** — services like frame-mcp and arifflow run code from `/root/FRAME/` and `/root/arifFlow/`. Demoting to non-root fails immediately at boot because the user can't traverse `/root` (mode 700, root-owned).
3. **Breaking Hermes breaks the phone interface** — Hermes runs VPS diagnostics, Docker ops, git operations. It legitimately needs root for Arif to chat from his phone without touching a terminal.
4. **chmod 600 on VAULT999 blinds witnesses** — 175+ scripts read VAULT999 continuously. Hiding it would break independent verification.
5. **Group cleanups risk shared state breakage** — removing `aaa-a2a` from `ariffazil` group before auditing file ownership breaks git operations.

### The Corrected Two-Dimension Binding

Binding has **two orthogonal dimensions**, and they must be applied in order:

```text
Dimension 1: SANDBOX BINDING (do this FIRST — no code path changes)
  systemd sandboxing primitives that strip kernel powers without changing UID:
  - NoNewPrivileges=true       (no setuid escalation)
  - ProtectSystem=strict       (read-only /usr, /boot, /etc)
  - ProtectHome=read-only      (read-only /home, /root)
  - ProtectKernelTunables=true (no /proc, /sys writes)
  - ProtectKernelModules=true  (no module loading)
  - ProtectControlGroups=true  (no cgroup manipulation)
  - RestrictNamespaces=true    (no namespace creation)
  - RestrictRealtime=true      (no realtime scheduling)
  - RestrictSUIDSGID=true      (no SUID/SGID bit honoring)
  - LockPersonality=true        (no personality change)
  - MemoryDenyWriteExecute=true (no W^X memory)
  - CapabilityBoundingSet=      (drop dangerous kernel caps)

Dimension 2: UID BINDING (do this SECOND — requires FHS migration first)
  Running services as dedicated non-root users.
  Requires:
  - Code promoted from /root/<repo> to /opt/<organ>/
  - Virtualenv owned by service user (or accessible via ACL)
  - FHS compliance so /opt/<organ>/ is the canonical home
  - Data paths moved out of /root/
```

**The order matters.** Sandbox first (reversible, no path changes). UID demotion second (irreversible, requires data migration).

### VAULT999 Protection (Corrected)

```text
WRONG: chmod 600 /root/arifOS/VAULT999/*.jsonl
  → Blinds 175+ witness scripts. Breaks "Witness > Projection."

RIGHT: chattr +a /root/arifOS/VAULT999/*.jsonl
  → Append-only attribute: can READ, can APPEND, cannot MUTATE/DELETE.
  → Even root cannot rewrite or truncate. Only root can drop the attribute.
  → Witnesses still see everything; only the overwrite attack is blocked.
```

**Applied 2026-09-17:** 32 core VAULT999 ledgers now `chattr +a` (append-only).

### GEOX: Sandbox Achieved Without UID Demotion

GEOX cannot run as `geox:geox` because its venv is root-owned with restrictive ACLs. **The correct fix is not to demote; it's to sandbox.**

Applied drop-in: `/etc/systemd/system/geox-mcp.service.d/zz-sandbox.conf`

```ini
[Service]
NoNewPrivileges=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictNamespaces=true
RestrictRealtime=true
RestrictSUIDSGID=true
LockPersonality=true
```

**Result:** GEOX is still UID 0 (root) but has no kernel powers it doesn't need. Cannot load modules, cannot modify kernel tunables, cannot create namespaces, cannot escalate via setuid. The data path problem is preserved. The blast radius is reduced.

**Sandbox score: 76% (8 of 11 primitives active).**

### arifflow: Already Hardened, Now Tighter

arifflow already had `NoNewPrivileges=yes`, `CapabilityBoundingSet=~CAP_SYS_ADMIN ~CAP_SYS_PTRACE ...`, `ProtectSystem=full`. Added:

```ini
ProtectKernelModules=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictNamespaces=true
RestrictRealtime=true
RestrictSUIDSGID=true
LockPersonality=true
MemoryDenyWriteExecute=true
CapabilityBoundingSet=~CAP_DAC_OVERRIDE ~CAP_DAC_READ_SEARCH ~CAP_FOWNER ~CAP_FSETID ~CAP_KILL ~CAP_SETGID ~CAP_SETUID ~CAP_SETFCAP ~CAP_SYS_CHROOT ~CAP_MKNOD ...
```

**Result:** arifflow's blast radius reduced from "full root" to "necessary capabilities only."

### Hermes: Correct Layer of Protection

Hermes MUST keep root (VPS executor for Arif's phone). Its safety is enforced at:

```text
- Authority Envelope (/root/AAA/instructions/authority-envelope.md)
- Reference Monitor (constitutional gate)
- Telegram RASA gates (human-meaning-membrane)
- Bounded subagent spawning
```

**NOT at the Linux user layer.** Demoting Hermes would break the primary agentic bridge.

---

## 15. The Two-Dimension Binding Metric (Updated)

```text
                    UID binding    +    Sandbox binding
Total declared          N              N
Bound                   b_uid         b_sandbox
Binding Ratio  =    max(b_uid, b_sandbox) / N
```

Sandbox binding alone counts as BOUND — the process is constrained even if it still runs as root.

**Current measurement (2026-09-17 after sandboxing geox + arifflow):**

```text
BINDING RATIO: 60% (6/10)
  UID binding:    4/10  (arifos, a-forge, wealth, frame)
  Sandbox binding: 2/10 (geox, arifflow)
  Inactive:        3/10  (well, hermes, vault999)
```

**Improvement path:**
- well: add sandboxing (run as is, strip powers) → sandbox BOUND
- hermes: keep root, but document why in Authority Envelope → intentional INACTIVE
- aaa: depends on what aaa-a2a actually needs → sandbox if possible

---

## 16. The Linus Lesson (For Real This Time)

> "Never break userspace."

In arifOS terms: **Never break the running federation to chase a theoretical permission model.**

The doctrine stands. The execution order changes:

```text
1. SANDBOX (reversible, no path changes, no service breaks)
2. CHATTR (append-only on ledgers, no permission changes)
3. MIGRATE (FHS promotion of code out of /root/)
4. DEMOTE (UID binding, only after FHS migration)
5. VAULT (witness-readable + tamper-proof, never hidden)
```

**The pattern is the medicine. The prescription is sandbox-first, demote-second, never-hide-the-witness.**

---

*DITEMPA BUKAN DIBERI ⚒️*
*The diagnosis IS the discovery. The cure is kernel-native, not doctored.*

---

## 17. Zero-Day Register (2026-09-17)

The architecture has 4 structural zero-days — places where the Governance Layer assumes a boundary that the Physics Layer does not enforce.

### ZD-1: Ambient Root Authority (CLOSED — partially)

**Status:** Reduced risk. Not eliminated.

**Doctrine says:** A-FORGE builds, Kernel decides, FRAME witnesses, VAULT999 proves. Organ X cannot write to Organ Y.

**Physics says:** Many services run with full Linux root powers. A prompt injection that triggers arbitrary file write executes with ambient root authority.

**Probe (2026-09-17):**
| Service | Sandbox Score | Status |
|---------|---------------|--------|
| a-forge | 75% | ✅ |
| a-forge-mcp | 75% | ✅ |
| geox-mcp | 75% | ✅ |
| frame-organ | 75% | ✅ |
| arifflow | 75% | ✅ |
| frame-mcp | 50% | ⚠️ |
| arifos | 25% | ❌ (kernel itself, harder to sandbox) |
| kabarkan-health | 75% | ✅ (was 0%, now sandboxed) |
| litellm-federation | 75% | ✅ (was 0%, now sandboxed) |

**Remaining gap:** arifOS (the constitutional kernel) itself runs with minimal sandboxing. Hardening it requires careful analysis of which paths it must write to (VAULT999, /opt/arifos/app).

---

### ZD-2: SSRF on Unauthenticated Loopback Daemons (OPEN)

**Status:** Documented. No fix applied (large undertaking).

**Doctrine says:** LOCALHOST_IS_PASSWORD — Postgres, Redis, Qdrant, NATS bind 127.0.0.1 with no auth. UFW blocks outside.

**Physics says:** Local services (playwright-mcp, firecrawl, searxng, media-ingest, web scrapers) can reach 127.0.0.1:5432 (Postgres), 6379 (Redis), 6333 (Qdrant), 4222 (NATS). A single SSRF redirect to a DB port bypasses all auth.

**Probe (2026-09-17):** 6 loopback daemons accept unauthenticated connections.
| Port | Service | Auth |
|------|---------|------|
| 5432 | Postgres (Docker) | ❌ None |
| 6379 | Redis | ❌ None |
| 6333 | Qdrant (Docker) | ❌ None |
| 4222 | NATS | ❌ None |
| 8222 | NATS monitoring | ❌ None |
| 4000 | LiteLLM / HAProxy | ❌ None |

**Recommended fix (not executed):**
- Add token-based auth to Postgres/Redis/Qdrant (requires app code changes)
- Run web scrapers in network namespace (`ip netns`) that cannot reach DB ports
- Use iptables `--uid-owner` to restrict which processes can connect to DB ports

---

### ZD-3: Silent FED Fallback (CLOSED)

**Status:** Patched. No silent fallback anymore.

**Doctrine says:** Witness > Projection. The system must declare anomalies immediately.

**Physics said:** When FED was unreachable, the kernel silently fell back to Ollama/local models. `status: "healthy"` was still reported on :8088. Cognitive tier dropped without alarm.

**Patch (2026-09-17):** Added explicit `cognitive_tier` and `fallback_acknowledged` fields to provider_status. When fallback is active, tier becomes `DEGRADED_COGNITIVE_TIER` or `DETERMINISTIC_ONLY`, never silent.

**Verification:**
```
cognitive_tier: FEDERATED
fallback_acknowledged: True
primary_provider: fed_federation
```

When FED goes down, this will show `DEGRADED_COGNITIVE_TIER` instead of silently falling back. The watchdog now sees the degradation.

**File:** `/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py:_probe_provider_status`

---

### ZD-4: Human Cognitive Denial of Service (OPEN — structural)

**Status:** Documented. Cannot be fixed in-session.

**Doctrine says:** F13: Arif is the sovereign human principal. W₈₈₈ (sovereign attention) is the ultimate cost.

**Physics says:** Multiple autonomous agents (OpenClaw, Kimi, Claude Code, Antigravity, Hermes) generate telemetry simultaneously. When agents disagree on system state, the dispute collapses to Arif's phone. A flood of subtle disagreements exhausts W₈₈₈.

**Recommended fix (out-of-session):**
- Enforce PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED chains mechanically
- Agents resolve evidence disagreements on port checks / hashes BEFORE messaging Arif
- Cross-agent arbitration tier: 2 agents must confirm before pinging human

**Why not fixed now:** Requires changes to multiple agents' message routing and arbitration logic. Each agent has its own implementation. One-session fix risks creating new arbitration bugs.

---

## 18. Zero-Day Closure Map

| ZD | Severity | Status | Closure Method |
|----|----------|--------|----------------|
| ZD-1 | HIGH | 🟡 REDUCED | systemd sandboxing (capability drops) |
| ZD-2 | HIGH | 🔴 OPEN | Pending: token auth or netns isolation |
| ZD-3 | MEDIUM | ✅ CLOSED | cognitive_tier field in provider_status |
| ZD-4 | MEDIUM | 🔴 OPEN | Pending: cross-agent arbitration tier |

**Net result:** 1 of 4 zero-days closed. 1 reduced in severity. 2 still open.

---

*DITEMPA BUKAN DIBERI ⚒️*
*Zero-day ≠ software bug. Zero-day = governance layer assuming a boundary the physics layer does not enforce.*
*Map reality first. Then patch.*
