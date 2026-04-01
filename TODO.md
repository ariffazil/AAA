# TODO.md — Kernel Task Queue (000–099)
> **Rule:** All tasks MUST pass the Kernel Filter

---

## 🔧 Kernel Filter Criteria (000–099 Band)

Before working on ANY task, verify ALL are true:
- [ ] **Compounds:** Effect builds over time
- [ ] **Strategic:** Revenue-linked or mission-critical
- [ ] **Substantial:** Takes 1+ week to build properly

**If ANY fail → SKIP, move to next task**

---

## 🎯 Active Queue (Prioritized)

### 1. 🟢 Implement LobsterLock Security Monitor
**Status:** Ready to start
**Compound:** Yes — continuously protects
**Strategic:** Yes — security is foundational
**Substantial:** Yes — multi-layer system

**Description:**
Create event-driven security monitoring for OpenClaw using semantic reasoning:
- Collector layer: audit, logs, fs-watcher
- Signal buffer for context accumulation
- Claude reasoning on triggers (not polling)
- Verdicts: CLEAR | WATCH | ALERT | KILL

**Next Action:**
Create `/root/waw/scripts/lobsterlock-monitor.js`

---

### 2. 🟡 arifOS Kernel Documentation
**Status:** Pending
**Compound:** Yes — docs enable scaling
**Strategic:** Yes — onboarding & sovereignty
**Substantial:** Yes — comprehensive system docs

**Description:**
Document arifOS Trinity architecture for future agents:
- 000–999 infrastructure band specifications
- Meta-Agent orchestration patterns
- Constitutional enforcement mechanisms
- VAULT999 audit trail format

**Next Action:**
Create `/root/waw/docs/arifOS-kernel-spec.md`

---

### 3. 🟡 Git Auto-Sync for waw
**Status:** Pending
**Compound:** Yes — prevents future breakage
**Strategic:** Yes — workspace integrity
**Substantial:** Yes — robust sync system

**Description:**
Implement bidirectional git sync for waw workspace:
- Pre-commit symlink verification
- Auto-resolve common conflicts
- Health check integration
- Rollback on sync failure

**Next Action:**
Create `/root/waw/scripts/git-sync-guard.sh`

---

### 4. 🟠 Model Routing Optimization
**Status:** Pending
**Compound:** Yes — saves money continuously
**Strategic:** Yes — cost efficiency
**Substantial:** Yes — intelligent routing logic

**Description:**
Optimize LLM usage by task type:
- Reasoning → Opus
- Code gen → Codex
- Bulk/heartbeat → MiniMax
- Fallback chain on rate limits

**Next Action:**
Update `openclaw.json` with task-based routing

---

### 5. 🔴 VAULT999 Integration
**Status:** Pending
**Compound:** Yes — audit trail accumulates
**Strategic:** Yes — constitutional requirement
**Substantial:** Yes — Merkle-sealed system

**Description:**
Integrate OpenClaw actions with VAULT999:
- Log significant actions with hashes
- Merkle tree for tamper evidence
- Periodic seal operations
- Query interface for audits

**Next Action:**
Design VAULT999 logging schema

---

## ✅ Completed (Archive Pattern)

### 2026-03-31 — OpenClaw Autonomous Recovery
- [x] Fixed broken symlinks from git sync
- [x] Implemented 4-file brain (AGENTS, SOUL, MEMORY, HEARTBEAT)
- [x] Configured compaction (prevents crashes)
- [x] Set up 30min heartbeat with silent mode
- [x] Created daily 5 AM self-heal cron
- [x] Aligned with arifOS Trinity principles
- [x] Restored from vanilla state

---

## 🗂️ Archive

Move completed tasks here after 30 days. Keeps queue focused.

---

**Motto:** *Kernel tasks forge infrastructure. Everything else is noise.* [000–099 | ΔΩΨ]
