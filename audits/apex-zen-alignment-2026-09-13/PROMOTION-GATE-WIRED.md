# PROMOTION GATE — WIRED (2026-09-13)
Invariant enforced: "No metric may be promoted unless it is backed by a witness object."
- Session-file records: require match against /root/VAULT999/apex-zen-witness.jsonl sources.
- Ledger-sourced records (arifFlow:*): witness = the metabolic ledger itself.
- DOWNGRADE/VIOLATION actions on UNWITNESSED records are WITHHELD (log_only + action_withheld=true).
Patch: scripts/apex-zen-consequence-router.py (backup *.bak-20260913-gate). Test: isolated output verified.
