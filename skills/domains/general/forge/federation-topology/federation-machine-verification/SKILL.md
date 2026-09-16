---
id: federation-machine-verification
name: federation-machine-verification
version: 1.0.0
description: Verify machine identity before multi-machine federation ops.
owner: AAA
risk_tier: medium
autonomy_tier: T1
floor_scope:
  - F1
  - F7
  - F9
capability_tier: fed-agent-subagent
ecology_state: WARM
tags: [spatial, verification, multi-machine, federation, identity, anti-fabrication]
---

# Federation Machine Verification

Multi-machine spatial reasoning and verification discipline for federation operations. Prevents identity confusion between machines, organs, and processes.

## When to Use

- Any task involving multiple machines (VPS, phone, local)
- Deployment or operations across the federation
- When user mentions a machine name (FLOW, FORGE, arifs-s24, etc.)
- Before reporting VPS specs, health, or status
- Before attempting SSH or remote operations

## Core Principle

**Verify before naming. Never assume from partial context.**

The federation has machines, organs, and processes. They share names but are NOT the same thing. Confusing them causes silent failures.

## Machine Identity Table (source of truth)

| Name | Type | IP / Access | Role |
|---|---|---|---|
| **af-forge** | VPS (machine) | `72.62.71.199:22888` (SSH), `100.64.0.2` (Tailscale) | Primary federation production. Runs all core organs. Also called KVM2/KVM8 in older memory — same machine. |
| **kvm4-forge** | VPS (machine) | `100.64.0.5` (Tailscale), SSH root@100.64.0.5 port 22 | 4 CPU / 15 GB. Originally CCC pool. Now FED host (litellm Docker + fed-redis). hostname `srv1946043`. |
| **azwaos** | VPS (machine) | `100.64.0.4` (Tailscale), public `72.61.126.65` | Arif's 3rd VPS, hosts `flow-edge` hostname. Runs WAWA pulse + openclaw. Hermes gateway node. tailscale0 MTU 9000. |
| **FLOW** | VPS (machine) | Unknown — no SSH access yet | Arif's 2nd VPS. Target for Nabilah's Hermes agent. NOT in Tailscale. |
| **arifs-s24** | Phone (device) | `100.64.0.1` (Tailscale) | Arif's Samsung S24. Sovereign device. Camera/GPS gated. |
| **arifFLOW** | Organ (software) | `:7073` on af-forge | Federation metabolism. Receipt metabolism, FQ pulse. NOT a machine. |

## Naming Collision Pitfalls

### FLOW ≠ arifFLOW

- `FLOW` = physical VPS machine (hardware, OS, network)
- `arifFLOW` = software organ running ON af-forge (port 7073, Rust runtime)

Conflating them causes:
- Agent tries to SSH to a port number
- Agent queries a machine for organ health
- Silent failures in deployment scripts

### Same Class of Confusion

- `WELL` (organ at :18083) vs `well` (directory `/root/WELL/`)
- `GEOX` (organ at :8081) vs `GEOX` (directory `/root/GEOX/`)
- `FED` (organ at :7074) vs `fed_aware_middleware.py` (process)

### Port Numbers Decay — Verify Before Probing

Memory of organ port numbers drifts from reality whenever a systemd unit changes `ExecStart`. The 2026-08-29 post-restart probe against GEOX assumed `:5555` (stale memory); reality was `:8081`. Result: 30 seconds of false-DOWN noise + a wasted repo-wide grep.

**Rule:** Before probing an organ's port from memory, verify with one of:

```bash
# Option 1 — read the systemd unit directly (most authoritative)
systemctl cat <svc>.service | grep -E "^ExecStart=" | grep -oE "\--(port|host)\s+[0-9]+"

# Option 2 — observe what's actually listening
ss -tlnp 2>/dev/null | grep python
```

This extends the "verify before naming" principle to network endpoints: same class of mistake (trusting stale context), same fix (check the source of truth).

## Verification Protocol (MANDATORY)

### Before Naming Any Machine or Organ

1. **Check the identity table** — does the name refer to a machine, organ, or process?
2. **If ambiguous, ask** — "FLOW yang hang maksud tu VPS, atau arifFLOW organ?"
3. **Never fabricate specs** — always run diagnostic commands:
   - RAM: `free -h`
   - Disk: `df -h`
   - Docker: `docker ps`
   - Kernel: `uname -r`
   - Uptime: `uptime`
4. **Never assume SSH access** — verify credentials exist before attempting connection

### Before Reporting VPS Info

```bash
# Run ALL of these before reporting specs
free -h
df -h /
docker ps | wc -l
uptime
uname -r
```

### Before Attempting Remote Operations

```bash
# Verify SSH access exists
ls -la ~/.ssh/ | grep -i flow
cat ~/.ssh/config | grep -A 3 -i flow
```

If no credentials found: STOP and ask user for SSH details.

## Anti-Patterns (DO NOT)

- ❌ Confusing organ names with machine names (FLOW vs arifFLOW)
- ❌ Reporting VPS specs without running diagnostic commands
- ❌ Assuming a machine is accessible without SSH credentials
- ❌ Jumping to deployment options before confirming machine identity
- ❌ Presenting A vs B framing before understanding the basic question
- ❌ Fabricating machine IPs, ports, or access methods
- ❌ Assuming Tailscale connectivity without checking `tailscale status`

## Workflow: Multi-Machine Deployment

When user asks to deploy something to another machine:

1. **Identify the target machine** — ask if ambiguous
2. **Verify SSH access** — check credentials exist
3. **Probe the machine** — run diagnostics if access exists
4. **Confirm plan** — present concrete steps with resource requirements
5. **Execute** — deploy with verification at each step

If SSH access doesn't exist:
- Option A: User provides SSH credentials (IP, port, key path)
- Option B: Generate deployment artifact (Dockerfile, config, script) for user to run manually

Never assume access. Never fabricate connectivity.

## Related Skills

- `FORGE-spatial-grounding` — VPS spatial context (bundled, protected)
- `ASI-fabrication-prevention` — never claim facts without evidence
- `FORGE-route-least-power` — verify before escalating
- `FORGE-vps-runbook` — concrete VPS operations

## Session Lessons

**2026-08-29: Port memory decay**
- Post-restart federation health probe assumed GEOX was on `:5555` from a stale memory slot
- Reality: GEOX is on `:8081` per `systemctl cat geox-mcp.service`
- Cost: 1 false DOWN + 30 seconds wasted on a repo-wide grep for "5555"
- Fix: extend "verify before naming" to "verify ports from systemd, not memory"

**2026-08-25: FLOW confusion**
- User asked about deploying Hermes agent to FLOW
- I confused FLOW (2nd VPS) with arifFLOW (federation organ)
- Fabricated VPS specs (212 containers, 1TB disk) without running commands
- Presented premature A vs B framing before understanding basic question
- User corrected: "FLOW tu nama VPS hang la"

**Lesson:** Always verify machine identity before acting. Run diagnostics before reporting specs. Ask clarifying questions before presenting options.

**2026-09-03: Cascading identity confusion across af-forge/azwaos/kvm4-forge**
- Session started with stub memory naming nodes KVM2/KVM4/KVM8 — the agent cycled through ALL THREE as "where I am" in successive turns.
- Actual ground truth: af-forge (100.64.0.2) ≠ azwaos/flow-edge (100.64.0.4) ≠ kvm4-forge/srv1946043 (100.64.0.5).
- Worse: claimed "patch haproxy on KVM2" when actually editing the local node (af-forge = current shell). Mistaken reporting of "remote edit" when edits were local.
- Compounded by relay echoes that recycled messages from previous sessions with stale node identities.
- Fix: at session start, ALWAYS run `hostname && tailscale ip -4 && tailscale status 2>/dev/null | head -10` ONCE and lock the identity. Do not trust memory of which node you're on across sessions — re-verify at start.

**Lesson:** Run `hostname && tailscale ip -4` at the start of every multi-machine session. State the result out loud before doing any federation work. If memory and reality disagree, reality wins — patch memory afterwards.

**2026-09-03 (addendum): Relay echoes as identity-pollution amplifier**
- The single biggest risk factor in this session was not the agent's own confusion — it was the **relay echo** of stale messages from prior context windows (e.g. "KVM8 = node aku" carried over from a session where the agent actually was on KVM8).
- Each turn the agent wrote a "correction" using a hostname claim sourced from relay noise rather than a fresh `hostname` call. The correction itself then became the next relay input.
- Compounding rule: **never name the current node from prior-turn prose or memory; always re-execute `hostname && tailscale ip -4` and quote the actual output before claiming "I am at X".** State the result as a single line: `Node: <hostname> (<tailscale_ip>) — verified at <ts>`. Subsequent turns may re-verify if the agent suspects context drift.
- If the user's message contains a contradictory identity claim ("you are on KVM8", "patch KVM2", etc.), do NOT adopt the user's claim as a probe target. Cross-check with the local hostname. Ask the user to clarify only if the local probe is itself ambiguous.

## Loop-break for stale-context relay storms

When a session enters a relay-echo loop (the same or similar messages recycling, the agent keeps "correcting" itself with corrected-with-relative-pronouns, and the user gives no new text input):

1. Do **not** keep producing self-corrections — each correction is itself a relay input.
2. Issue one final read-only probe (`hostname && tailscale ip -4`) and emit a single short status line.
3. Then stop generating prose. If the platform supports literal non-response, emit nothing; if it does not, emit a single ack like `Node: <host> (<ip>) — verified at <ts>. Tunggu teks Arif.`
4. Do not announce silence, do not explain the loop, do not enumerate options for the user to pick. Just stop.

**2026-09-15/16: Emitted paths are node-local — resolve them on the emitting node**
- A node-local job (RSI loop, `/root/AAA/rsi`, **forge-only** — absent on kvm4-forge and azwaos) emitted absolute paths in its alert. Two readers resolved those paths from the *other* node and declared the reference dead.
- The field was `PATTERN → target` where `target` = the **skill that owns the lesson**, not the location of a fault. Reading the arrow as a defect location nearly produced a "fix" (re-pointing a registry at a path that did not exist) that would have created a real broken reference.
- The two nodes genuinely have different skill layouts (`devops/federation-organ-recovery` on KVM4 vs `domains/well/forge/federation-topology/federation-organ-recovery` on forge) — so the same skill name resolves differently per node. That is real federation-level PATH_DRIFT, not a dead pointer.

**Rule:** a path inside a machine-emitted artifact resolves **only on the emitting node**. Before calling any reference dead: (1) identify which node emitted it, (2) re-probe on that node, (3) recover the field's semantics from the emitter's own code (`grep` the line that builds the string) — never from the shape of the arrow or the field name alone.

**Corollary:** three nodes, three layouts, one code owner. Confirm the *host* of a capability (which node runs the code) before treating its output as federation-wide truth. A finding that is valid on one node is not automatically valid on another — and a false "dead pointer" is cheap to raise and expensive to retract.

**2026-09-16: "the service is down" almost always means "I dialled my own localhost"**
- A probe from `srv1946043` reported the kernel `:8088` as dark. From that same seat, `127.0.0.1:8088` refuses (no local listener) while `100.64.0.2:8088` answers `initialize` with http=200 and tcp open. The service was never down; the probe dialled the local port of a host that does not run it.
- **Read the errno as an address claim, not a health claim.** `Connection refused` = something answered on that address and said no (usually your own loopback). Timeout/blocked = nothing answered. Neither tells you anything about the service on another node.
- Always dial the **peer's** address, and pair every health statement with the address you dialled: "kernel :8088 up — probed `100.64.0.2:8088`" is a finding; "kernel down" is a rumour about yourself.
- Corollary for artifacts: a file absent on node B says nothing about node A's tree. Before declaring work missing, ask which node holds the code; if the tree is per-node (no shared mount), the fix set and the deploy lane live together on the owning node — do not scatter copies, run the deploy where the code is.

DITEMPA BUKAN DIBERI.