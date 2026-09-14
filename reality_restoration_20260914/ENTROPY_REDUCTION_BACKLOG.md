# Entropy Reduction & Reality Restoration Backlog (Phase I)
**Document:** `ENTROPY_REDUCTION_BACKLOG.md`  
**Standard:** QQQ Protocol · Prioritized Action Plan  
**Date:** 2026-09-14T09:54:00+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::ENTROPY_REDUCTION::REALITY_GRAPH::v1`

---

## 1. Actionable Backlog

### Category 1: Quick Wins (Digital / MUBAH · Minimal Risk · Instant Execution)
| Task ID | Action Description | Entropy Removed | Blast Radius | Reversibility | Authority / Mechanism |
|---|---|---|---|---|---|
| **QW-01** | **Add `ReadWritePaths=/root/.aforge` to `a-forge-mcp.service.d/override-audit-path.conf`** and run `systemctl daemon-reload && systemctl restart a-forge-mcp`. | Resolves P0 EROFS crash on `forge_vps_ports` and `forge_vps_services`. | BR-1 (Local unit) | REV-5 (Delete line to revert) | Pre-authorized Digital Bugfix |
| **QW-02** | **Purge 24 `flame_*` rule IDs and alias `low` effort in `/root/.config/federation-models.json`**. | Eliminates dead-end FLAME routes for low-effort tasks. | BR-1 (Config file) | REV-5 (Git revert) | Pre-authorized Hygiene |
| **QW-03** | **Enforce `chmod 600` on 144 Hermes subagent logs** in `/root/.hermes/cache/delegation/`. | Eliminates world-readable prompt leaks. | BR-0 (Permissions) | REV-5 (Trivial chmod) | Pre-authorized Security |
| **QW-04** | **Prune 4 legacy RG2 worktree directories** from `/root/forge_work/worktrees/`. | Frees disk clutter and aligns worktree directory with active leases. | BR-1 (Scratch dirs) | REV-5 (Non-git scratch) | Pre-authorized Clean |

---

### Category 2: Medium Effort (Configuration & Fallback Elevation)
| Task ID | Action Description | Entropy Removed | Blast Radius | Reversibility | Authority / Mechanism |
|---|---|---|---|---|---|
| **ME-01** | **Elevate DeepSeek ($14.28 balance) and MiniMax (Token Plan Max) to top fallback rungs** in `/root/A-FORGE/litellm-config.yaml` above exhausted 429/402 tiers. | Cuts 3–5 seconds of retry latency across all federation LLM calls. | BR-2 (LiteLLM routes)| REV-4 (Config revert) | Pre-authorized Optimization |
| **ME-02** | **Rename LiteLLM container `nervous_visvesvaraya` to `fed-litellm-kvm8`**. | Restores canonical naming in Docker process table. | BR-1 (Container name)| REV-5 (Rename command) | Pre-authorized Hygiene |

---

### Category 3: High Impact (Requires F13 Sovereign Ratification)
| Task ID | Action Description | Entropy Removed | Blast Radius | Reversibility | Authority / Mechanism |
|---|---|---|---|---|---|
| **HI-01** | **Formal Decommissioning of 6 Orphan Services** (`agentgateway-shadow` and 5 `apa-*-bridge` units). | Prevents systemd failure storm on next machine reboot. | BR-3 (Daemons) | REV-3 (Service files archived) | **F13 Ratification** (F9 ANTI-HANTU gate) |
| **HI-02** | **Off-Box Replication of Sovereign State (`/root/.hermes`)**. | Eliminates single-disk failure domain on `/dev/sda1` for 1.6GB Hermes credentials and state. | BR-2 (Rsync network)| REV-5 (Rsync exclude tokens) | **F13 Ratification** (External data transfer) |

---

### Category 4: Architectural (Long-Term Swarm Substrate)
| Task ID | Action Description | Entropy Removed | Blast Radius | Reversibility | Authority / Mechanism |
|---|---|---|---|---|---|
| **AR-01** | **Unify Hermes `mem0` Vector Storage into SRO Witness Substrate**. | Reconciles 14,399 un-witnessed memory points into governed federation collections. | BR-4 (Memory DB) | REV-3 (Dual-write phase) | Architectural / F13 |
| **AR-02** | **Enforce Path-5 Worktree Substrate on all Multi-Agent Sessions**. | Permanent elimination of the "two writers, one file" conflict across all FI coder citizens. | BR-2 (Workflows) | REV-5 (Path-5 engine live) | **SEAL_CAPABILITY** achieved |
