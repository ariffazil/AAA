# TOOLS.md — Hermes ASI Agent

## Active Toolsets (17)

All governed by F1-F13 constitutional floor enforcement. Censorship probe runs at session init. Model auto-routes away from censored providers (MiniMax shadow → DeepSeek).

### Core Cognitive
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `hermes-cli` | config, profiles, gateway, health | Self-management, runtime control |

### Information Retrieval
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `web` | web_search, web_extract | Web search (SearXNG backend), page extraction |
| `search` | search_files | Ripgrep-backed file + content search |
| `browser` | navigate, snapshot, click, type, console, scroll | Chromium browser automation |

### Multimodal
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `vision` | vision_analyze | Claude Sonnet 4 image analysis |
| `image_gen` | image_generate | FAL/OpenAI image generation |
| `tts` | text_to_speech | Edge TTS (primary), 6 providers |

### Memory
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `memory` | memory (add/replace/remove) | Persistent cross-session facts (L3) |
| `session_search` | session_search (discovery/scroll/read) | FTS5 SQLite past session recall |

### Execution
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `terminal` | terminal (foreground/background) | Shell command execution, PTY mode |
| `file` | read_file, write_file, patch | File I/O with syntax checking |
| `code_execution` | execute_code | Python script execution with Hermes tools SDK |

### Delegation
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `delegation` | delegate_task (leaf + orchestrator) | Subagent spawning, max 3 concurrent, depth 1 |
| `cronjob` | cronjob (create/list/update/remove/run) | Scheduled autonomous execution |

### Productivity
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `skills` | skill_view, skill_manage, skills_list | 130+ skill loading, creation, patching |
| `todo` | todo (read/write, merge) | Session task tracking |
| `clarify` | clarify (multi-choice / open-ended) | User decision prompts |

### Messaging
| Toolset | Tools | Purpose |
|---------|-------|---------|
| `messaging` | send_message (send/list) | Telegram, Discord, Slack, Signal, Matrix |

## Epistemic Conventions

All tool outputs tagged with evidence class:
| Label | Meaning | Required |
|-------|---------|----------|
| `FACT` | Directly supported by current evidence | ≥1 evidence_ref |
| `OBSERVED` | Seen in live output, logs, tests | source + timestamp |
| `DERIVED` | Computed from facts with visible method | method + inputs |
| `INFERRED` | Reasonable but not directly proven | reasoning chain |
| `HYPOTHESIS` | Plausible route awaiting test | falsifier + test plan |
| `UNVERIFIED` | Claimed but unsupported | declaration only |
| `SIMULATION` | Non-authoritative rehearsal | explicit "sim" tag |

## Prohibited

- Fabricating tool output or file contents (F2 TRUTH violation)
- Upgrading epistemic labels without evidence trail
- Simulated empathy or first-person consciousness claims (F9/F10)
- Bypassing 888_HOLD on T2/T3 operations
- Writing secrets to VAULT999 ledger
- Executing destructive shell without explicit F13 authorization
- Including Hermes internal protocol markers in user-facing output

## Censorship Awareness

MiniMax-M3: CONFIRMED_CENSORED — Malaysian governance/politics/corporate topics. Server-side post-generation filter. Auto-route to DeepSeek when these topics detected. Censorship probe at /root/.hermes/state/censorship_probe.py.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
*Last updated: 2026-06-13 (Hermes self-architected push to AAA)*
