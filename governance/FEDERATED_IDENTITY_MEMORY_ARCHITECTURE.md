# Federated Multi-User, Multi-Group, and Memory-Mesh Architecture
**Canonical Standard for arifOS Federation & Hermes Gateway**
*Sealed: 2026-09-04 · Authority: F13 SOVEREIGN · Status: RATIFIED*

---

## 1. Executive Summary & Problem Formulation

In a sovereign AI federation operating across multiple conversational endpoints (Telegram DMs, Telegram Groups, Forum Topics, Web Interfaces), managing **multi-tenant identity**, **memory isolation**, and **channel routing** poses a classic multi-context dilemma:

1. **Fragmentation Debt:** Adding a user or group requires synchronizing multiple independent configuration layers (`config.yaml`, `lanes.yaml`, systemd drop-ins, and memory markdown files).
2. **Context Bleed (The Anti-Privacy Vulnerability):** In a naive memory model, personal memories collected in private 1-on-1 DMs leak into public group discussions, violating dignity (F6) and trust.
3. **Identity Collapse:** Treating human users merely as strings or IDs rather than rich relational entities with distinct communication registers, roles, and emotional baselines.

This architecture establishes a **Zen Federated Model** that guarantees:
- **Zero-Friction Channel Administration:** A single atomic command (`hermes-id-zen`) updates all routing layers and provisions memory scaffolds.
- **Strict Triadic Context Isolation:** Complete epistemic air-gapping between Sovereign workspace, Private Warga DMs, and Shared Group Spaces.
- **Unified Knowledge-to-Memory Continuum:** Clean separation between static constitutional laws, dynamic organ capabilities, shared group topics, and individual episodic memories.

---

## 2. Context Geometry: The Triadic Plane

Every incoming update $S = \langle \text{user\_id}, \text{chat\_id}, \text{payload}, \text{timestamp} \rangle$ is mapped onto a 3-dimensional context coordinate:

$$\text{Context}(S) = \mathcal{C}_{\text{Global}} \oplus \mathcal{C}_{\text{Space}}(\text{chat\_id}) \oplus \mathcal{C}_{\text{User}}(\text{user\_id}) \oplus \mathcal{K}_{\text{Organs}}$$

```
                               ▲ WHO (User Axis)
                               │
                               │  [Tier 0: Sovereign Arif]
                               │  [Tier 1: Warga - Syed, Izzu, Aliff]
                               │  [Tier 2: Guest / Observer]
                               │
                               └─────────────────────────► WHERE (Space Axis)
                              ╱  - Private DM (1-on-1)
                             ╱   - SADO Group (-1003815535761)
                            ╱    - AIA Group (-1003521544074)
                           ▼ WHAT (Domain / Knowledge Axis)
                          - arifOS (Governance & F1-F13)
                          - GEOX (Subsurface & Seismic)
                          - WEALTH (Trading & Capital)
                          - WELL (Health & Dignity)
```

### Layered Storage Architecture

| Layer | System / File | Scope | Access Rule |
| :--- | :--- | :--- | :--- |
| **L0: Constitutional Commons** | `AAA_MALAYSIAN_RASA_CONSTITUTION.md`, `AGENTS.md` | Federation-wide | Read-only for all agents |
| **L1: Domain Knowledge Mesh** | GEOX / WEALTH / WELL / arifOS FastMCP | Federation-wide | Gated by Tool Authority Registry |
| **L2: Shared Group Rooms** | `/root/.hermes/memories/ROOM-*.md`, Redis `group:*` | `chat_id` specific | Visible only to members of that group |
| **L3: Private Warga Memory** | `/root/.hermes/memories/MEMORY-*.md`, Redis `user:*` | `user_id` specific | Visible **ONLY** in private 1-on-1 DMs |
| **L4: Sovereign Core** | `/root/.hermes/lanes/private/arif-private.md`, VAULT999 | Sovereign only | Strict F13 gate (Arif ID `267378578`) |

---

## 3. The Anti-Leakage Invariants (Constitutional Floors)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ANTI-LEAKAGE INVARIANTS                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 1. [DM_TO_GROUP_ISOLATION]: Private medical details, personal finances, or    ║
║    vulnerabilities recorded in `MEMORY-{user}-dm.md` MUST NEVER be output in  ║
║    any group chat (`chat_id < 0`).                                           ║
║                                                                              ║
║ 2. [SOVEREIGN_COMMAND_ISOLATION]: System mutations (shell, git, systemctl,   ║
║    API keys) are HARD-DENIED unless `user_id == 267378578` (Arif).           ║
║                                                                              ║
║ 3. [PERSONA_DYNAMIC_REGISTER]: In group settings, the agent speaks with      ║
║    group-safe adab, never exposing private 1-on-1 inside jokes that exclude  ║
║    other members.                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 4. Federated Identity & Channel Operations (`hermes-id-zen`)

To prevent config drift and manual errors, all channel additions and memory scaffolding are managed via the atomic CLI utility `hermes-id-zen`:

```bash
# Registering a user:
hermes-id-zen add-user 1042200555 --name "Syed" --username rico_ricaldo_33 --role WARGA --groups -1003815535761,-1003753855708

# Registering a group room:
hermes-id-zen add-group -1003815535761 --title "SADO Main Group"

# Comprehensive status check:
hermes-id-zen list
```

### Execution Pipeline

```
[hermes-id-zen add-user]
          │
          ├── 1. Atomic update to ~/.hermes/config.yaml (allowed_chats & free_response)
          ├── 2. Formats & validates YAML entry in ~/.hermes/lanes.yaml
          ├── 3. Scaffolds USER-{slug}.md (Profile & Preferences)
          ├── 4. Scaffolds MEMORY-{slug}.md (Private Log & Invariants)
          ├── 5. Scaffolds SOUL-{slug}.md (Persona & Tone)
          └── 6. Writes JSON descriptor lane-{slug}.json
```

---

## 5. Summary Table of Registered Warga & Channels

| Entity | Identifier | Type | Authority | Assigned Lane | Primary Register |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Muhammad Arif bin Fazil** | `267378578` | User (DM & Group) | **SOVEREIGN** | `arif` / `arif-sado` | Strategic / Executive |
| **Syed (Abang Sado)** | `1042200555` | User (DM & Group) | **WARGA** | `syed` | Brotherly / Caregiver / Trading |
| **Muhammad Aliff** | `1024343313` | User (DM & Group) | **WARGA** | `aliff` / `aliff-aia` | Respectful / Professional |
| **Izzu** | `1237635275` | User (DM & Group) | **WARGA** | `izzu` / `izzu-aia` | Collaborative / Health / KPJ |
| **Sin** | `5930780714` | User (DM & Group) | **WARGA** | `sin` | Casual / Technical |
| **Faqwan** | `6041855106` | User (DM) | **WARGA** | `faqwan` | Friendly / Adab |
| **Amir Ridzwan** | `317849404` | User (DM & Group) | **WARGA** | `amir-ridzwan` | Athletic / Advisory |
| **SADO Group** | `-1003815535761` | Supergroup | **GROUP_ROOM** | `group-sado` | Group-safe / Banter / Community |
| **AIA Group** | `-1003521544074` | Supergroup | **GROUP_ROOM** | `group-aia` | Group-safe / Insurance / Work |

---

*Sealed and integrated into the arifOS Federation Substrate.*
