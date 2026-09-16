# Federation Record Surfaces — What Each One Actually Holds

Ordered by how often a subject is found there. Sweep all of them before asserting absence.

| Surface | Holds | Notes |
|---|---|---|
| `/root/.hermes/memories/MEMORY.md` | sealed profile entries: people, groups, environment traps | the canonical short-form record; injected into every session |
| `/root/.hermes/memories/USER.md` | the sovereign's own profile/preferences | person entries about others belong in MEMORY.md |
| `/root/.hermes/output/` | forged artifacts — dossiers, PDFs, HTML, previews | send with `MEDIA:/abs/path`; check for stale versions |
| `/root/.hermes/config.yaml` | lane allowlists (`allowed_chats`, `allow_from`, `group_allow_from`), `require_mention` | may be auto-rewritten by the runtime — never the sole authority |
| `/root/.hermes/.env` | same allowlists, exported form | a distinct surface from config.yaml |
| `/root/.secrets/kunci-mas.flat.env` | the same allowlists again | the systemd `EnvironmentFile` — on this host the runtime reads THIS one; edits elsewhere are silently ignored. Verify against the live process environ |
| `/root/.hermes/workspace/zen/`, `mem0-promotion-ledger.jsonl`, `mem0_dump.jsonl` | long-term memory promotions, older session facts | JSONL — grep with a windowed pattern, not `cat` |
| `/root/.hermes/logs/` (`gateway.log`, `agent.log`) | live traffic, who said what in which chat | useful for confirming a lane actually receives messages |
| `/root/.hermes/lanes/`, `/root/HERMES/lanes/private/` | lane definitions and private relationship files | private files are scar-gated and read-only once canonized |
| `/root/HERMES/cache/documents/` | inbound document cache (chat exports, pasted files) | a small pointer file may reference a very large export here |
| `/root/AAA/` (reports, memory, scars, canon, governance) | session reports, doctrines, registries, scar records | `reports/` and `memory/` carry dated session summaries |

## Sweep pattern

```bash
# 1. shape sweep (respects ignore rules — expect a hidden-match warning)
#    search_files(pattern='<name>', target='files')  +  target='content'
# 2. hidden sweep (grep does not respect ignore rules)
grep -ril '<name>' /root/.hermes/memories/ /root/.hermes/workspace/ /root/.hermes/logs/ 2>/dev/null | head -20
ls -la /root/.hermes/output/
grep -io '.\{0,150\}<name>.\{0,250\}' /root/.hermes/mem0-promotion-ledger.jsonl | head
# 3. identifier variants — same subject, different keys
#    full name · short name · social handle · Telegram uid · chat/group id
# 4. routing confirmation (if the subject is a lane member)
grep -n '<uid-or-chat-id>' /root/.hermes/config.yaml /root/.secrets/kunci-mas.flat.env
```

## Identity keys are separate records

One subject appears as: legal name, short/familiar name, social handles per platform, a numeric
uid, and one or more chat/group ids. Each key retrieves a different set of files. A lookup that
used one key is a partial probe — say so, or run the rest.
