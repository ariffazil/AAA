# Full Telegram Enumeration Audit — 2026-08-29

## Method

Probed live via Telegram Bot API (`getChat`, `getChatMemberCount`, `getMe`) against
`@ASI_arifos_bot` (id: 8410138119). Cross-referenced with:
- `/root/.hermes/config.yaml` (allowed_chats, free_response_chats)
- `/root/.hermes/lanes/lanes.yaml` (persona lane triggers)
- `/root/.hermes/skills/federation/telegram-bot-routing-doctrine/SKILL.md` (P2 table)

## Groups (14 total: 13 supergroups + 1 channel)

| #  | Chat ID            | Name                    | Type       | Members | Lane?      | free_resp |
|----|--------------------|-------------------------|------------|---------|------------|-----------|
| 1  | -1003753855708     | AAA                     | supergroup | 7       | no         | yes       |
| 2  | -1003815535761     | SADO                    | supergroup | 3       | YES        | yes       |
| 3  | -1003768847825     | Kanak-kanak             | supergroup | —       | no         | yes       |
| 4  | -1003792478194     | Dear NABILAH            | supergroup | —       | no         | yes       |
| 5  | -1003521544074     | AIA                     | supergroup | 5       | no         | yes       |
| 6  | -1003721331017     | Al AMIN                 | supergroup | —       | no         | yes       |
| 7  | -1004446358629     | arifOS                  | channel    | —       | no         | yes       |
| 8  | -1003749710464     | BODYBUILDER             | supergroup | 4       | no         | yes       |
| 9  | -1003890512851     | makcikGPT               | supergroup | 6       | YES        | yes       |
| 10 | -1003747272167     | Syed Sado Agent Client  | supergroup | 3       | no         | yes       |
| 11 | -5443591163        | YANG ARIF               | supergroup | —       | YES        | yes       |
| 12 | -1004397386934     | Sin Boy                 | supergroup | 3       | YES        | yes       |
| 13 | -1003979217026     | PROPA                   | supergroup | 4       | no         | yes       |
| 14 | -1004301943630     | Analyst                 | supergroup | 3       | no         | yes       |

## Private Users (13 total: 6 named + 3 unnamed + 4 stale)

| #  | User ID     | Name                    | Lane(s)              | Authority | Capabilities               |
|----|-------------|-------------------------|----------------------|-----------|----------------------------|
| 1  | 267378578   | Arif (ariffazil)        | arif                 | SOVEREIGN | FULL                       |
| 2  | 1042200555  | Syed (rico_ricaldo_33)  | syed + syed-dm       | WARGA     | ADVISORY + TRACKING        |
| 3  | 1024343313  | Muhammad Aliff          | aliff + aliff-aia    | WARGA     | ADVISORY + TRACKING        |
| 4  | 1237635275  | Izzu                    | izzu + izzu-aia      | WARGA     | ADVISORY + TRACKING        |
| 5  | 5930780714  | Sin (@Sin)              | sinboy + sinboy-group| WARGA     | ADVISORY (shadow)          |
| 6  | 6041855106  | Faqwan                  | faqwan               | WARGA     | ADVISORY + TTS + IMAGE     |
| 7  | 788277295   | Ayu                     | (none)               | TAMU      | free_response only         |
| 8  | 8324190535  | Wawa                    | (none)               | TAMU      | free_response only         |
| 9  | 5250473787  | Amin                    | (none)               | TAMU      | free_response only         |
| 10 | 5316953867  | STALE                   | —                    | —         | API: "chat not found"      |
| 11 | 8798431893  | STALE                   | —                    | —         | API: "chat not found"      |
| 12 | 5444180135  | STALE                   | —                    | —         | API: "chat not found"      |
| 13 | 1639470103  | STALE                   | —                    | —         | API: "chat not found"      |

## Corrections from This Audit

1. **BODYBUILDER chat_id:** Routing doctrine listed `-5561731065`. Live API confirms correct ID is `-1003749710464`. The `-5561731065` was never a valid supergroup ID.

2. **4 stale user IDs** in config.yaml that return "chat not found":
   - 5316953867, 8798431893, 5444180135, 1639470103
   - Candidate for removal from `allowed_chats` + `free_response_chats`

3. **3 unmapped users** (Ayu, Wawa, Amin) have free_response access but no lane persona.
   - They get guest-level (TAMU) replies only.
   - If richer behavior is needed, add lane entries in lanes.yaml.

4. **Routing doctrine P2 table** was 9 groups / 3 DMs. Actual surface is 14 groups / 13 users.
   - The doctrine needs a full P2 table update (patch blocked — user-owned skill).
   - Recommend: `hermes curator adopt telegram-bot-routing-doctrine` then patch.

## Cron Delivery Targets (from cronjob list)

| Target             | Job Count | Key Jobs                                        |
|--------------------|-----------|------------------------------------------------|
| Arif DM (267378578)| 13        | morning-pulse, world-reality-intel, reckoning,  |
|                    |           | morning-brief (M/W/F + rest), geo-econ-horizon,|
|                    |           | iron-radar, arifflow-digest, evening-zen-brief, |
|                    |           | vps-backup, reddit-monitor, malaysia-intel,     |
|                    |           | upstream-drift-watch                            |
| Syed DM (1042200555)| 4        | mak-cbd-followup, mak-dressing, gerd-log,       |
|                    |           | sambal-preorder                                 |
| Local only         | 8         | attestation-check, metrics-pulse, trajectory,   |
|                    |           | seal-sweep, drift-audit, stale-cleaner,         |
|                    |           | vision-densify, forge-vault-ingest              |

## Config Cross-Reference Summary

- `allowed_chats`: 26 entries (14 groups + 12 user IDs)
- `free_response_chats`: 26 entries (same set)
- `require_mention`: false (global Telegram setting)
- `lanes.yaml` mapped: 12 lane entries covering 6 named users + 2 group personas + 1 ghost group + 1 guest catchall
- Orphan chats (free_response but no lane): 10 groups + 3 users
