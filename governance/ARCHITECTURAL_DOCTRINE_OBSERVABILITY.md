# ARCHITECTURAL DOCTRINE: CONSTITUTIONAL OBSERVABILITY (SOT-HUD-001)

> **Authority:** arifOS Sovereign Federation · F1 Truth & Amanah  
> **Status:** RATIFIED & SEALED  
> **Date:** 2026-08-15  
> **Canonical Path:** `/root/AAA/governance/ARCHITECTURAL_DOCTRINE_OBSERVABILITY.md`  
> **DITEMPA BUKAN DIBERI**

---

## 1. The Core Invariant (The First Law)

```text
LIVE PROBE OR UNKNOWN.
NEVER PRETEND.
```

An agent system is not a simulation of certainty; it is an apparatus for navigating uncertainty.
Printing a decorative metric (e.g., hardcoding `FQ: 0.99` or `Pending HOLDs: 0` without probing) is a **critical violation of Floor 1 (Amanah) and Floor 2 (Truth)**.

A constitutional HUD must safely print:
```text
FQ: UNKNOWN [NO_PROBE]
```
and retain full integrity. The moment a HUD displays fake state, agents stop trusting the substrate.

---

## 2. The 5-Panel Cognitive Abstraction

When an agent spawns, it does not need a chaotic 10-screen dump. It requires five sequential answers:

```text
1. IDENTITY    → Who am I?       (SCT Token, Lane, Actor ID, Session Root)
2. AUTHORITY   → Can I?          (Autonomy Tier T0–T3, Lease Boundary, Sovereign Veto)
3. SURVIVAL    → Am I safe?      (RAM, Disk, Load, Organ Health Grid, Active Holds)
4. JUDGMENT    → What blocks me? (F1–F13 Constitutional Floors, ΔS ≤ 0, P(truth) ≥ 0.99)
5. MISSION     → What next?      (Evidence Grounding, Carry Forward Focus, Task Delta)
```

### Hierarchy of Needs:
* **Authority precedes Action:** Permission must be evaluated before intent.
* **Survival precedes Mission:** An unstable runtime cannot execute high-risk mutations.
* **Evidence precedes Confidence:** No mission status without live proof.

---

## 3. The 3-Stage Pipeline (Decoupled SOT Architecture)

```text
┌────────────────────────┐      ┌─────────────────────────┐      ┌────────────────────────┐
│   LIVE STATE ENGINE    │ ───> │  CANONICAL STATE FILE   │ ───> │     PURE RENDERER      │
│ (Probe / Telemetry)    │      │  (JSON / SOT on Disk)   │      │ (Terminal HUD / MOTD)  │
└────────────────────────┘      └─────────────────────────┘      └────────────────────────┘
```

1. **State Engine (`generate-session-briefing.sh` / `now` / `doctor.sh`):**
   - Probes live ports (`:8088`, `:7071`, `:8081`, `:18082`, `:18083`).
   - Counts real git commits and uncommitted diffs.
   - Evaluates active `.hold` files and VAULT999 sealed events.
2. **Canonical State File (`carry_forward.json` / `state.json`):**
   - Pure serialized truth.
   - Stamped with ISO-8601 UTC timestamps.
3. **Pure Renderer (`06-arif-live` / `briefing`):**
   - Zero recalculation logic.
   - Zero hardcoded assumptions.
   - Fast, resilient rendering with timeout wrappers.

---

## 4. Protocol Against Future Agent Violations

To prevent future agents from introducing hardcoded telemetry or fake state:

### A. Non-Bypassable Static Telemetry Rule
Any script or MOTD component that emits telemetry **must derive the value from a live execution or print `UNKNOWN`**.
* ❌ `printf "FQ: 0.99\n"` (Hardcoded string) $\rightarrow$ **FORBIDDEN (F1/F2 VOID)**
* ✅ `val=$(curl -s ... | jq .fq // "UNKNOWN")` $\rightarrow$ **ALLOWED (F1 Truth)**

### B. MOTD & Login Hygiene
* `/etc/update-motd.d/05-arifos` is **decommissioned** (purged of hardcoded values).
* `/etc/update-motd.d/06-arif-live` is the **sole live cockpit MOTD** (sub-second parallel live probe).
* `/usr/local/bin/briefing` is the **canonical session handoff tool** (`generate-session-briefing.sh`).

### C. Agent Handoff Command
Every new session start must anchor itself via:
```bash
briefing 24   # Reviews the last 24 hours of git delta, seals, holds, and carry-forward state
```

---

## 5. Summary Table of Tools & Ownership

| Surface | Tool / Script | Role | SOT Source |
|---|---|---|---|
| **Login MOTD** | `/etc/update-motd.d/06-arif-live` | Real-time system/organ health | Parallel live curl & proc probes |
| **Session Handoff** | `/usr/local/bin/briefing` | Multi-repo git & seal delta | Git logs, VAULT999, `carry_forward.json` |
| **Temporal Anchor** | `/usr/local/bin/now` | Time & federation state pulse | NTP, system clock, kernel FQ |
| **Public Atlas** | `https://arif-fazil.com/world/` | Real GIS Macro & Geopolitical Atlas | Leaflet WGS84, CartoDB, Esri Satellite |

---
*DITEMPA BUKAN DIBERI · F1 AMANAH · F2 TRUTH · F13 SOVEREIGN*
