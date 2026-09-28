---
name: hermes-federated-identity
description: "Federated multi-user, multi-group, identity routing, and memory partition controller for Hermes in arifOS."
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

### Group-Driven Admission (F13 declares a third party for care)

When the sovereign (Arif, F13) declares a third party inside a shared group as a care-target ("ni anak aku nak jaga"), admission requires **two coordinated writes** — `hermes-id-zen add-user` only handles the dm path:

1. **`/root/.hermes/lanes/people.yaml`** — append a `people.<slug>` entry with:
   - `display_name`, `dm_lanes: []` (zero — no DM until they message),
   - one `identities` row with `kind: telegram_user_id`, `value: '<id>'`, `source: 'arif (F13 sovereign), YYYY-MM-DD'`, `observed: YYYY-MM-DD`,
   - one `facts` row stating F13's relation (e.g. "kanak-kanak jaga Arif") with `scope: shared` so the lane card can carry it in shared rooms where that person appears. Default `scope: dm` blocks shared-room injection.
2. **`/root/.hermes/config.yaml`** — append the id to `telegram.allowed_chats`. Without this, group messages from that id are ignored at the gateway.
3. **Reload** — gateway restart from inside the process is blocked (SIGTERM propagates); Arif must `ssh vps` + `hermes gateway restart`, or schedule a one-shot delay.

Pitfall: never write `identities` with `value: '<id>'` only — `kind` and `source` are required by the admission rule, and missing them fails the spec. Pitfall: setting `scope: dm` for a care-target keeps them invisible in the group where they live — set `scope: shared` if F13 wants group-aware persona.

Pitfall: gateway checks `telegram.allowed_chats` BEFORE reading `lanes/people.yaml`. If F13 declares a new ID and you only patch `people.yaml`, the gateway still silently drops their messages. Always append to BOTH files in the same write — never split them across turns or sessions. After both writes, verify with `grep '<id>' /root/.hermes/config.yaml` before declaring admission complete.

Pitfall: gateway restart from inside the running gateway process is blocked (SIGTERM propagates and kills the restart command). Two paths out: (1) Arif runs `hermes gateway restart` from a separate shell, or (2) schedule a one-shot `systemctl restart hermes-gateway.service` via `terminal(background=true)` so the parent session isn't the one calling restart. Never tell the user "restart done" if you couldn't actually issue the restart — check via `systemctl status` after the delay.

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
