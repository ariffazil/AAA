# Multi-User Federation — Mode A/B Design (2026-08-09)

Session outcome: Arif asked "can one agent know both my reality and Syed's (and other humans/agents) yet federated — theory of mind level?" Answer forged: YES, via a Person Register (index + edges, DER-labeled) while raw reality stays in each person's lane. He then chose **Mode A first** (one agent serves all, zero config for humans), **Mode B later** (per-human agents) — because "most human cannot manage their own agent pening kepala" and Abang Sado has no time to configure anything.

## The core move

**knowing-about ≠ owning.** Profiles/vaults = who owns raw memory. Person Register = the agent's models of each person. Theory of mind is holding a model of another mind *as a model* — with F7 humility that the model is smaller than the person, always.

## The register file (forged this session)

`/root/AAA/federation/person-register.json` (v1.0.0, valid JSON, 3 persons + 5 edges):

- `persons`: ARIF (267378578, F13, sovereign), SYED (1042200555, lane /root/sado/, dossier + mak-health + trading + brand), WAWA (8324190535, skeleton — UNKNOWN, no lane)
- `edges`: ARIF⇄SYED kawan/trading · SYED→MAK_ROSNANI caregiver · SYED→JEREMY_TOH tenant · ARIF→WAWA UNKNOWN · ARIF→FEDERATION sovereign
- `routing`: tg_user_id match → that person's lane + voice register; no match → main lane
- Fields per person: voice_register, lane_root, canonical refs, boundaries (scars/tenancy/autonomy), state snapshot

Schema shape worth reusing: `register_version / created / description / sovereignty / mode / mode_note / epistemic_rule / persons[] / edges[] / routing`.

## Hermes mechanics verified (docs + gateway source, 2026-08-09)

Source of truth: `gateway/run.py` (`profiles_to_serve`, `_start_secondary_profile_adapters`, `_profile_runtime_scope`) + `gateway/config.py` (`multiplex_profiles`, `profile_routes`) + docs user-guide/{profiles, profile-distributions, multi-profile-gateways}.

| Capability | What it does | Verified |
|---|---|---|
| `gateway.multiplex_profiles: true` | One gateway process serves default + every named profile. Per-turn scope: config, skills, memory, SOUL, **and credentials** resolved per routed profile. Sessions namespaced `agent:<profile>:` (default keeps `agent:main:`). | docs + run.py:2973, 9069 |
| `gateway.profile_routes` | Shared-bot chat → profile routing: match most-specific-first (thread_id > chat_id > guild_id), all fields AND. Works on every platform adapter. | docs + config.py |
| Token locks | Two profiles polling same (platform, token) → second refuses with error naming the conflicting profile. | docs + run.py claimed[] |
| `/p/<profile>/` prefix | HTTP-inbound (webhook/api_server/etc.) for secondary profiles on the shared listener. Secondary profiles must NOT bind ports in multiplex mode. | docs |
| Profile distributions | `hermes profile install github.com/... --alias` — one command installs SOUL/config/skills/cron/mcp.json from git. Installer hard-excludes auth.json, .env, memories/, sessions/, state.db. Update keeps user-owned files. **This is the Mode B enabler.** | docs |

## Real-world findings (OBS)

- The aaa-hermes profile config (`allow_from`) already whitelisted Syed (1042200555) — meaning the sovereign agent was already serving a 2nd human with full sovereign memory in context. Leak was live, not theoretical.
- Existing per-profile homes on this host: `default`, `aaa-hermes` (active), `hermes_apex`, `hermes_asi`, `hermes_forge` — the federation was already running separate agent personas; only aaa-hermes has a running gateway.
- `lane_switch.py` in this skill hardcodes `LANE_REGISTRY` — the skill's own docstring says to replace with a JSON file read. The register file now exists; rewiring is pending T1.

## Sequence to implement Mode A (reversible, T1)

1. Register already forged ✅
2. Flip `gateway.multiplex_profiles: true` on the owning profile + gateway restart (T2, announce)
3. Create clean profiles for each human (own memory, no scar tools, no federation hooks)
4. Remove non-operator IDs from sovereign profile's `allow_from` (closes live leak)
5. BotFather: one new bot token per human profile (Arif's 2-min action)
6. Rewire `lane_switch.py` → read register
7. B later: author per-human distribution repo, `hermes profile install` once

DITEMPA BUKAN DIBERI.
