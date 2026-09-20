# Cross-Registry Reconciliation Pattern

> When multiple registries describe the same entity class, their disagreement is the first finding.

## When to use

Any task that involves: multiple data sources describing the same entities (humans, services, agents, machines), discrepancy identification, unified view creation, and ongoing monitoring.

## Procedure

1. **Enumerate all registries.** Search for files that look like registries: `find <root> -name "*register*" -o -name "*registry*" -o -name "*roster*" -o -name "*cards*" | grep -v node_modules`. Don't assume you know them all.

2. **Extract entity lists from each.** For each registry, pull: entity ID, display name, any external identifiers (telegram ID, email, IP), status fields, timestamps.

3. **Cross-reference on the external identifier.** Match entities across registries using the most stable external key (numeric IDs > display names > descriptions). Build a merge table.

4. **Classify each entity by coverage:**
   - **Full** — present in 2+ registries with consistent data
   - **Partial** — present but with mismatched fields (wrong ID, stale name, missing facts)
   - **Ghost** — present in registry but zero evidence of real interaction
   - **Orphan** — real interaction exists but no registry entry
   - **Reclassified** — entity was wrong type (bot classified as human, service classified as agent)

5. **Fix bugs immediately.** Remove ghosts, reclassify mis-typed entities, correct wrong IDs. These are data-quality bugs, not governance decisions.

6. **Create unified view.** One registry that merges all sources. Tier by interaction recency:
   - Tier 1: live interaction (recent DM/API call)
   - Tier 2: group interaction only
   - Tier 3: referenced in memory/docs only, no live path

7. **Build heartbeat scaffold.** For each entity: last interaction timestamp, dependency health, alert threshold. Store as JSON with a versioned schema.

8. **Define alert thresholds.** Time-based escalation: OK (0-3 days) > WATCH (4-7) > FLAG (8-14) > ESCALATE (15-30) > CRITICAL (30+).

## Pitfalls

- **Don't trust display names as unique keys.** The same person can appear as "al", "Aliff", "ALIFF", and "Aliff Husna" across registries. Match on numeric/external IDs, not names.
- **Bots in human registries are common.** When a bot DM session has a display name, registries may classify it as a human. Check the session origin field (user_id vs bot_id) to verify.
- **Stale registries are worse than no registry.** A registry last updated months ago creates false confidence. Date-stamp every registry and flag if older than the review cycle.
- **A registry without a heartbeat is an address book.** Timestamps on creation are not telemetry. The value is in last-interaction recency, not in how many fields the card has.
- **Cross-registry work requires fresh reads.** Don't rely on cached registry content from earlier in the conversation. Re-read each file before writing the unified view.

## Output format

1. Audit report (markdown) with: executive summary, cross-reference matrix, bugs found, unified registry, heartbeat spec, recommendations
2. Cleaned registries (fix bugs in-place)
3. Heartbeat scaffold (JSON with versioned schema)

## Example use case

Human registry audit: HAMPA (15 humans, stale July 2026) vs person-register.json (6 persons, August 2026) vs Telegram sessions (12 DM users, live). Found: 1 bot misclassified as human, 1 ghost entry, 1 identity collision, 7 humans with zero interaction path.