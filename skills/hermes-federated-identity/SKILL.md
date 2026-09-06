---
name: hermes-federated-identity
description: "Federated multi-user, multi-group, identity routing, and memory partition controller for Hermes in arifOS. Use when adding/managing Telegram user IDs, group IDs, creating person/group lanes, inspecting allowed chats, or auditing memory isolation between private DMs and public groups."
version: 1.0.0
tags: [identity, multi-user, multi-group, telegram, memory-partition, lanes, hermes]
capability_tier: fed-long-context
ecology_state: WARM
---

# Hermes Federated Identity & Memory Partition Doctrine (Zen Architecture)

> **DITEMPA BUKAN DIBERI — F13 SOVEREIGN GOVERNED**
> Single Source of Truth for Multi-User, Multi-Group, and Memory-Mesh orchestration across Telegram and Hermes.

---

## 1. The Multi-Context Geometry (Context Triad)

Every incoming message to Hermes resolves along three orthogonal axes:

```
                      ┌────────────────────────┐
                      │  WHO (User Context)     │
                      │  - user_id / username  │
                      │  - Authority Tier      │
                      │  - Personal Persona    │
                      └───────────┬────────────┘
                                  │
                                  ▼
┌────────────────────────┐  RESOLVED CONTEXT  ┌────────────────────────┐
│ WHERE (Space Context)  │ ═══════════════════ │ WHAT (Knowledge Mesh)  │
│ - DM vs Shared Group   │                     │ - Organs (GEOX/WEALTH) │
│ - Room Topic Memory    │                     │ - F1-F13 Constitution  │
│ - Anti-Leakage Boundary│                     │ - Malaysian RASA Model │
└────────────────────────┘                     └────────────────────────┘
```

### Context Resolution Matrix

| Ingress Type | `user_id` | `chat_id` | Active Memory Files | Voice & Tone | Privacy Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sovereign DM** | `267378578` (Arif) | `267378578` | `MEMORY.md`, `USER.md`, `arif-private.md` | Strategic, direct, executive | **SOVEREIGN MAXIMUM** |
| **Warga DM** | E.g. `1042200555` (Syed) | `1042200555` | `MEMORY-syed.md`, `USER-syed.md`, `SOUL-syed.md` | Warm, unhurried, brotherly care | **CONFIDENTIAL DM** |
| **Shared Group** | Any registered user | E.g. `-1003815535761` | `ROOM-sado.md` + Group-safe User Register | Collaborative, group-safe, adab | **GROUP-SAFE (NO DM LEAK)** |
| **Guest / Public** | Unmapped ID | Any allowed chat | Default `MEMORY.md` (read-only minimal) | Polite, helpful, constrained | **GUEST (READ-ONLY)** |

---

## 2. The Anti-Leakage Law (F1 / F6 / F13)

1. **Private DMs are Air-Gapped:** Medical records, personal finances, intimate concerns, and private sovereign instructions from 1-on-1 DMs **MUST NEVER** be cited, referenced, or summarized in shared group chats.
2. **Group Memory is Scoped to Room:** Group discussions, jokes, and community plans belong in `ROOM-{group}.md` and Qdrant scope `group`.
3. **No Autonomous Mutation by Non-Sovereigns:** Only Arif (`267378578`, F13) has execution authority over shell commands, server infrastructure, or secret vaults. All other users receive advisory, coaching, and analytical assistance.

---

## 3. Atomic Tool: `hermes-id-zen`

To eliminate configuration fragmentation, use the canonical CLI tool `/usr/local/bin/hermes-id-zen`.

### Quick Commands

```bash
# 1. List all registered users, groups, authority tiers, and free-response status
hermes-id-zen list

# 2. Add a new Telegram user (atomically updates config.yaml + lanes.yaml + memory scaffolds)
hermes-id-zen add-user <USER_ID> --name "Nama Panggilan" --role WARGA --username handle

# 3. Add a new Telegram group room
hermes-id-zen add-group <GROUP_ID> --title "Nama Group"

# 4. Scan recent channel interactions
hermes-id-zen scan
```

### What `hermes-id-zen add-user` does automatically:
1. Appends `USER_ID` to `config.yaml` (`telegram.allowed_chats` & `free_response_chats`).
2. Registers a typed lane entry in `lanes.yaml` with appropriate triggers and voice register.
3. Generates `memories/USER-{slug}.md` (profile & communication preferences).
4. Generates `memories/MEMORY-{slug}.md` (private timeline & notes).
5. Generates `memories/SOUL-{slug}.md` (specific persona relationship).
6. Creates `memories/lane-{slug}.json` descriptor.

---

## 4. Hierarchy of Storage & Memory Systems

```
┌────────────────────────────────────────────────────────────────────────┐
│ L0: Constitutional Commons  (F1-F13, AAA Malaysian RASA Constitution) │
├────────────────────────────────────────────────────────────────────────┤
│ L1: Organ Knowledge Mesh    (GEOX, WEALTH, WELL, arifOS MCP Tools)     │
├────────────────────────────────────────────────────────────────────────┤
│ L2: Space / Room Memory     (/root/.hermes/memories/ROOM-*.md)         │
├────────────────────────────────────────────────────────────────────────┤
│ L3: Person / Lane Memory    (/root/.hermes/memories/MEMORY-*.md)       │
└────────────────────────────────────────────────────────────────────────┘
```

- **Ephemeral Context:** Redis keys `user:{slug}:*` and `group:{slug}:*`.
- **Semantic Long-Term:** Qdrant collections filtered by `subject: {slug}` or `scope: group`.
- **Audit & Receipts:** VAULT999 cooling ledger for critical sovereign decisions.
