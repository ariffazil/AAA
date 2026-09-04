# HERMES_CRON_BAN_DOCTRINE.md — Hermes cron BANNED, 4-scheduler doctrine (F13, 2026-09-04)

## Verdict
**Hermes MUST NOT register cron jobs.** Per Phase 2 default A8 ratification.

## Why
Cron is a 4th scheduler lane that bypasses arifOS L5 OPS doctrine:
- arifOS :7073 (Flow metabolism) — primary
- arifOS kabarkan (OTEL transport) — observability
- systemd-timers (per-node, proposal→ratified) — operations
- **cron = shadow lane, no governance binding, no F13 audit hook**

A cron job fires regardless of constitutional state. That's exactly the kind of
autonomous surface Hermes must not own.

## The 4-scheduler doctrine
| Scheduler | Owner | Scope | Constitutional binding |
|---|---|---|---|
| arifOS :7073 (Flow) | kernel | federation-wide | F1-F13 audited |
| arifOS kabarkan | OTEL | observability | F1-F13 audited |
| systemd-timers | per-node | operations | proposal→ratified via A-FORGE |
| **cron (BANNED for Hermes)** | — | — | **no binding, no Hermes ownership** |

## Migration plan
1. Identify all `/etc/cron.d/hermes-*` and root crontab entries touching Hermes
2. Convert each to systemd-timer with `OnCalendar=` equivalent
3. Wrap in unit that calls into arifOS /signal/inbox or /flow instead of bypassing
4. `.disabled` files: archive to `/etc/cron.d/.hermes-cron-ban-20260904/`

## Enforcement
- Phase 4 (KVM4 hygiene): install `hermes-cron-guard.sh` pre-commit hook that
  refuses to commit new `cron.d/hermes-*` entries
- Phase 5 (re-probe): scan for `crontab -l \| grep -i hermes` output = empty
- F13 violation = revert + receipt + musyawarah

## Reversibility
- `mv /etc/cron.d/.hermes-cron-ban-20260904/* /etc/cron.d/` restores old cron
- This doctrine is a doc, not enforced in code (yet — Phase 4 enforcement gate)

Refs: Hermes attention-theft remediation Phase 2 / A8.
