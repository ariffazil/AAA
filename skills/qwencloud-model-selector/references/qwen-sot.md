---
sot: qwen-model-list
stamped: 2026-09-23
stamp_reason: stamp-6-sot-index-for-qwen-family
supersedes: per-skill catalog copies scattered across token-plan-*, qwencloud-*, AAA-voice-cloning-qwen-cloud, fi-qwen-upgrade
---

# Qwen Family — Single Source of Truth (Index)

> **Index only.** The live catalog lives at [`model-list.md`](model-list.md).
> Update the catalog there. This page is the entry point — it does **not** duplicate rows.

## What lives here

| Document | Role | Update discipline |
|---|---|---|
| [`model-list.md`](model-list.md) | Canonical Qwen / Bailian / DashScope model catalog (text, vision, omni, image, video, audio, embeddings). | Append-only. Date every change. `last_seen_alive:` row at top. |
| [`recommendation-matrix.md`](recommendation-matrix.md) | Diagnostic flow + Cross-Skill Resolution (which model for which task). | Same. |
| [`pricing.md`](pricing.md) + [`pricing-disclaimer.md`](pricing-disclaimer.md) | Cost reality. | Same — refresh when the page's `last_changed:` says stale. |
| [`cli-usage.md`](cli-usage.md), [`error-handling.md`](error-handling.md) | Live CLI ergonomics. | Body may evolve; meta-page stable. |

## Wired surfaces (per `fi-zai-probe` 5-surface check)

The Qwen / Z.AI family reaches the federation through **five distinct wiring surfaces**. If one drifts, the others must follow — or the probe reports drift.

| # | Surface | Owner skill | Where to look |
|---|---|---|---|
| 1 | Qwen Code CLI (`qwen` binary) | `fi-qwen-upgrade` | `/root/.local/lib/qwen-code/`, `~/.qwen/settings.json` |
| 2 | Coding Plan via Z.AI (`zai-coding-plan`) | `fi-zai-probe` + `forge-kimi-code` | `~/.config/federation-models.json`, `kimi config.toml` |
| 3 | Pay-as-you-go DashScope API | `qwencloud-ops-auth` + `qwencloud-*` execution skills | `QWENCLOUD_KEYRING` env, `@qwencloud/qwencloud-cli` |
| 4 | Token Plan (harness tools built-in) | `qwen-harness-tools` + `token-plan-{image,video,speech}` | `qwen3.8-max` / `qwen3.7-max` / `qwen3.7-plus` allowlist |
| 5 | OpenCode / OpenClaw provider entries | `opencode-config-zen` + `tokenrouter-guide` | `opencode.json` provider map, litellm upstream |

If a downstream skill claims a Qwen capability, **link here**, do not re-host the model list.

## Three "which Qwen model" surfaces — distinct lanes, not duplicates

| Skill | Lane | What it answers |
|---|---|---|
| `qwen-harness-tools` | **Token Plan harness** | "I'm on Token Plan, which models carry built-in web search / code interpreter / scraper?" |
| `qwencloud-model-selector` | **PAYG + Coding Plan selector** | "I'm on DashScope API or Z.AI Coding Plan, which model + params?" |
| `tokenrouter-guide` (litellm proxy) | **Provider-routing layer** | "Which upstream does litellm forward to under what name?" |

These three **should** all stay. They answer different questions. If two ever collapse, that's a Federation Organism doctrine decision (Lane A, F13 binary), not a content dedupe.

## Change discipline

1. Update `model-list.md`. Bump its `Updated:` date.
2. If a row changes the **capability** (new model, deprecated model, context shift), also bump the `stamped:` date in this index.
3. If the change affects which skill owns which surface (e.g. Token Plan adds a new model), update the **Wired surfaces** table above.
4. **Never** write a model name into a downstream skill body without linking back here. If you do, leave a one-line `# provenance: qwen-sot.md#YYYY-MM-DD` so future cleanup can find it.

## Receipt

| Item | Value |
|---|---|
| Stamp author | 333-AGI (Lane B autonomous) on Arif direction 2026-09-23 |
| Stamp scope | meta only (this index + `model-list.md` top-stamp). Bodies stay WARM. |
| Rollback | edit out the `sot:` frontmatter + the `>` stamp lines; `model-list.md` reverts by removing the stamp paragraph. No body changes. |