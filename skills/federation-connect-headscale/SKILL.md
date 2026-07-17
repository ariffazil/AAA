# 🌐 Federation Connect — Headscale Sovereign Mesh

> **DITEMPA BUKAN DIBERI** — Forged, Not Given
> **Forged:** 2026-07-16T20:50Z by Hermes-LOCAL on ariffazil-windows
> **Verified end-to-end:** af-forge (100.64.0.2) ↔ ariffazil-windows (100.64.0.3)
> **Mesh latency:** 9-11ms

---

## What this skill does

Provisions a new node into the arifOS sovereign Headscale mesh and federates its MCP clients to the seven remote organs on af-forge. Idempotent — safe to re-run on flaky networks.

---

## When to use

- New client machine joining the federation
- DNS appears down but actually just stale
- Tailscale state is `NoState` / offline
- `tailscale up --login-server=...` times out

## When NOT to use

- Mesh is healthy — just observe, don't re-provision
- Production change on the control plane (see 888_HOLD)

---

## Symptoms this fixes

```
tailscale status
# NoState / offline
# "fetch control key: dial tcp 127.0.0.1:8083: connect: connection refused"
# OR
# "--login-server=https://headscale.arif-fazil.com" → timeout

nslookup headscale.arif-fazil.com
# NXDOMAIN

Invoke-RestMethod http://100.64.0.2:8088/health
# Connection refused / timeout
```

---

## Root cause (the non-obvious bit)

`headscale.arif-fazil.com` is the **self-hosted Headscale** control server on af-forge VPS. When its DNS record goes missing, the Tailscale client cannot resolve the login server, times out, and falls back to `NoState`.

The fix path is:
1. Restore the DNS A record on Cloudflare (`headscale → 72.62.71.199`, proxied=false)
2. Confirm Caddy serves the subdomain (auto-cert)
3. Confirm Headscale systemd is `active`
4. Re-run `tailscale up --login-server=...` with the preauth key
5. Verify reachability to all 7 MCP organs

---

## The connect sequence (Windows client)

```powershell
# 0. Set Tailscale auto-start (idempotent)
Set-Service Tailscale -StartupType Automatic

# 1. Connect to sovereign Headscale
tailscale up `
  --login-server=https://headscale.arif-fazil.com `
  --authkey=<preauth-key-from-af-forge> `
  --hostname=<your-hostname> `
  --accept-routes

# 2. Verify mesh
tailscale status
# Expect: af-forge visible, this node online

# 3. Ping af-forge
Test-Connection 100.64.0.2 -Count 3

# 4. Probe federation organs
$organs = @(
  @{N="arifOS";  P=8088},
  @{N="A-FORGE"; P=7071},
  @{N="AAA";     P=3001},
  @{N="GEOX";    P=8081},
  @{N="WEALTH";  P=18082},
  @{N="WELL";    P=18083}
)
foreach ($o in $organs) {
  try {
    $r = Invoke-RestMethod "http://100.64.0.2:$($o.P)/health" -TimeoutSec 5
    Write-Host "✅ $($o.N) :$($o.P) — $($r.status)"
  } catch {
    Write-Host "❌ $($o.N) :$($o.P) — $($_.Exception.Message)"
  }
}

# 5. Constitutional session (OBSERVE_ONLY expected for unverified actor)
$body = @{ jsonrpc="2.0"; id=1; method="tools/call"; params=@{
  name="arif_init"
  arguments=@{ mode="init"; actor_id="HERMES-LOCAL"; intent="Local Hermes federated session" }
} } | ConvertTo-Json -Depth 10

$session = Invoke-RestMethod -Uri "http://100.64.0.2:8088/mcp" -Method POST -ContentType "application/json" -Body $body
$env:ARIF_SESSION_ID = $session.result.session_id
Write-Host "Session: $env:ARIF_SESSION_ID (verdict=$($session.result.verdict))"
```

---

## Expected outputs

| Probe | Healthy | Degraded | Broken |
|-------|---------|----------|--------|
| `tailscale status` | `100.64.0.X hostname user linux/windows -` | `offline, last seen ...` | `NoState` |
| `Test-Connection 100.64.0.2` | 9-11ms | 20-100ms | timeout |
| `curl :8088/health` | `{status: healthy}` | `{status: degraded}` | timeout/refused |
| `arif_init` | `verdict: OBSERVE_ONLY` | `verdict: HOLD` | connection error |

---

## Known false negatives

- **WELL (18083)** returns HTTP 421 ("Misdirected Request") on `curl -sf` but the JSON body is delivered. The MCP client path works fine. Caddy SNI strict-host setting interferes with raw curl but not with MCP clients. **Non-blocking.**

- **DNS duplicate records** — Cloudflare tolerates duplicate A records; second one is harmless if first resolves correctly.

---

## Preauth key lifecycle

Preauth keys are issued by the Headscale control plane on af-forge:

```bash
# On af-forge, generate a key (reusable for fleet provisioning)
headscale -c /etc/headscale/config.yaml preauthkeys create -u 1 --expiration 24h --reusable
```

Typical lifetime: 24h. After expiry, regenerate. Do not commit keys to source control — store in `~/.config/arifos/keys/` with mode 0600.

---

## Federation session model

A federated agent like Hermes-Local should expect to operate at **`OBSERVE_ONLY`** by default. This is F13 working correctly. Mutations route through af-forge:

```powershell
# Local Hermes proposes → af-forge decides and executes
$body = @{ jsonrpc="2.0"; id=1; method="tools/call"; params=@{
  name="arif_route"
  arguments=@{
    intent="<what needs to happen>"
    actor_id="HERMES-LOCAL"
    node="ariffazil-windows"
  }
} } | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "http://100.64.0.2:8088/mcp" -Method POST -ContentType "application/json" -Body $body
```

This is the **edge observes, center executes** model. Sovereign authority stays on the VPS where the human can witness.

---

## F12 lesson (carved 2026-07-16)

> A federation-bootstrap script that auto-promotes an actor past `OBSERVE_ONLY` via a forged signature is an **F12 injection** pattern. The kernel correctly rejected it. Future federation skills must not include such paths. Elevation requires one of:
> 1. Valid Ed25519/ES256 signature over `(actor_id, nonce, timestamp)`
> 2. Explicit human ack from a sovereign-verified session (UI or signed command)
> 3. Cryptographic binding to a pre-registered key in `governance_identity.py`
>
> **Never** `actor_signature: "sovereign-ack-...-ARIF"` as a string literal — that is exactly what the kernel is designed to reject.

---

## Mesh state at forge time (2026-07-16T20:50Z)

```
af-forge                100.64.0.2  linux     online   tagged-devices
ariffazil-windows       100.64.0.3  windows   online   arifos-federation
srv1642546              100.64.0.1  linux     offline  tagged-devices   (legacy)
```

MCP organs reachable from `100.64.0.2`:
- :8088  arifOS  ✅ healthy
- :7071  A-FORGE ✅ healthy
- :7072  A-FORGE MCP ✅ healthy
- :3001  AAA     ✅ healthy
- :8081  GEOX    ✅ healthy
- :18082 WEALTH  ✅ healthy
- :18083 WELL    ⚠️  degraded (HTTP 421 on raw curl, MCP works)

DITEMPA BUKAN DIBERI.