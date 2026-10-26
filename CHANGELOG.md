# Changelog — AAA (Intelligence Routing & State Plane)

All notable changes to the AAA organ.

## [Unreleased]

### Fixed (Build)
- postcss.config.js: Scope `@tailwindcss/postcss` scanning to `base: './src'`. Eliminates recursive Oxide filesystem traversal over 47,000+ non-frontend files, reducing Vite build peak RSS from 7.63 GB (earlyoom SIGKILL 137) to 375 MB and build time from >4m48s to 2.72s.


### Security (preserved from live 2026-10-22 hardening, Git custody 2026-10-24)
- a2a-server: rightmost-only `X-Forwarded-For` loopback-proxy trust (spoof regression-tested from non-loopback peer)
- a2a-server: `anonymous` removed from `CANONICAL_ACTORS`; unsigned agent dispatch → 403 on both dispatchers; actor↔signer binding (accounting uses DID-verified organ)
- a2a-server: TDZ-safe `effectiveSourceAgent`; tasks/send replay guard; 5-min `issued_at` freshness
- federation_envelope: envelope actor-claim scope enforcement (fail-closed strict)
- identity: lowercase key deduped against canonical `333-AGI_public.pem`; actor registry synced
- Full record: `docs/A2A-AUTH-HARDENING-PRESERVATION-2026-10-24.md` · branch `preserve/live-auth-hardening-2026-10-24`

### Added
- MEMORY_ENGINEERING_SPEC_v1
- Witness Void Canon pointers in glossary

### Changed
- Canonical glossary updated with new pointers

## [2026.08.30] — AGI Substrate Integration

### Added
- 9-ATLAS genome integration
- AGI substrate assessment and readiness gates
- 3-surface contracts (A2A/MCP/Zen)

### Changed
- Federation structural correction (2026-08-14)
- State protocol audit completed

## [2026.08.14] — Federation v2 Compliance

### Added
- Federation V2 compliance report
- Agent card registry
- Agent surface map (YAML)

### Changed
- FLAME router operational
- MCP federation zen mapping

## [2026.07.19] — Governance Hardening

### Added
- F13 ratification packet
- Hold resolution (HOLD-01/02)
- Constitution matrix

### Changed
- Memory routing updated
- Agent init contracts formalized
