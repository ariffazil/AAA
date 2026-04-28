Arif wants verdicts only (✅ Done / ⚠️ SABAR / 🛑 VOID), no option lists. He fact-checks AI output hard — caught wrong file sizes, wrong Caddyfile ports, wrong mount paths. Always verify disk/API directly, never trust secondary sources. High visual bar — rejected "meh" dashboard, accepted same data with proper design. "Give it a hard refresh" was his practical cache solution.
§
VPS gateway: `openclaw-gateway` binary runs bare (no systemd). `hermes-asi-gateway` systemd service conflicts with it — disable with `systemctl disable hermes-asi-gateway`. One process owns Telegram polling.

arifosmcp.arif-fazil.com is a redirect gateway — 301 forwards all non-MCP paths to arifos.arif-fazil.com/mcp/. This is by design, NOT an outage. GET /mcp → 405 is correct (POST-only JSON-RPC).

geox/legacy_skills/ can disappear from disk (untracked deletion) but lives in git HEAD. `git checkout HEAD -- geox/legacy_skills/` restores it.