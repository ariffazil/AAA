# Observability Events

This directory defines the append-only event layer for AAA.

Each event should be serializable against:

- `schemas/event.schema.json`
- `schemas/audit-event.schema.json`

Core replay dimensions:

- `domain_plane`
- `integration_ref`
- `pipeline_stage`
- `band`
- `verdict`
- `vault_ref`
- `witnesses`
- `separation_of_duties`

Canonical replay path:

`workflow record -> event stream -> 888 judgment -> 999 vault ref`
