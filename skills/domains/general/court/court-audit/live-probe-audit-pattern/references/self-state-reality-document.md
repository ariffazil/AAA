# Self-State Reality Document — "who are you, as per reality now"
> **Provenance:** recovered 2026-10-23 from KVM4 (`/root/.hermes/skills/software-development/live-probe-audit-pattern/SKILL.md`) by `skills-catalog-drift.py`.
> This section existed on KVM4 and was **absent from the whole KVM8 tree** — a casualty of
> consolidation-by-heading rather than consolidation-by-content. Body is verbatim; nothing
> added. KVM8-side home chosen by subject, not by the peer's folder layout.

## Self-State Reality Document ("who are you, as per reality now")

**Signal:** the sovereign asks the agent to describe *itself* — "who are u", "forge a pdf about
yourself", "as per reality now". The deliverable is a measured self-state artifact, not a
personality essay.

**Rule set:**
- Probe the full inventory BEFORE authoring: host/uptime/load, the mouth process (`ps`, not just
  `systemctl is-active`), the model router, the kernel `/health` with per-floor status/score/
  provenance, skill count, MCP servers, cron enabled-vs-total, session/message counts.
- Report the floor board as **measured counts with named failures and named `unmeasured`**, never
  a green total. `floor_passed:false` means one floor closed the gate — it does not mean the
  system is broken, and it must not be softened.
- Include a numbered **"what is wrong today"** section. A self-report with zero defects is
  marketing, not witness.
- Carry-forward notes and memory are priors, not evidence — when a live probe contradicts a stale
  note, say so in the document.
- Counts are per-node. Name the host beside every number.

**Probe pitfall that costs a cycle:** `curl URL | python3 - <<'EOF'` discards the pipe — the
heredoc owns stdin, so `json.load(sys.stdin)` parses the script text and dies with
`JSONDecodeError: Expecting value: line 1 column 1`. Write to a file then read it (`curl -o
/tmp/x.json` + `python3 -c`), never heredoc-into-python while piping.

**Service-unit vs process:** `hermes-gateway` reading `inactive` while the gateway runs as a bare
`python -m hermes_cli.main gateway run` process is a normal shape here — report both readings and
the discrepancy, don't declare the mouth down from `systemctl` alone.

Full worked example (probe inventory, document shape, delivery): `references/self-state-reality-document-2026-10-23.md`.

