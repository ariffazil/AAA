# PHONE BODY STATE — 2026-10-19

> **Canonical owner of the phone-body fact.** All other surfaces point here.
> Author: 333-AGI. Evidence: live probes 2026-10-19 (OBS unless marked).
> Supersedes: phone-body assumptions in the 2026-10-18 carry-forward.

## 1. Bodies

| Body | Role | Tailnet | Bridge | State (OBS) |
|---|---|---|---|---|
| Honor 600 Pro | **ACTIVE main** | `100.64.0.6` | `http://100.64.0.6:8765` | health 200; battery 100%, 33.0 °C, 4443 mV, cycle 67; sensors live (`ak0991x` magnetometer); F-Droid Termux:API active |
| Samsung S24 | **STANDBY fixed** | `100.64.0.1` | `http://100.64.0.1:8765` | health 200; battery 100%, 39.6 °C, plugged AC |

- VPS client SOT: `/root/AAA/phone-bridge/.env` → Honor `.6`; `BRIDGE_USE_HTTPS=0`. Switch recorded in-file: **2026-09-29 14:0x MYT, S24 → Honor** (same day as localhost.run → Tailscale direct). Honor has been the canonical body since then.
- S24 fallback env backup: `/root/AAA/phone-bridge/.env.bak-s24-active-*` — do not switch without a reason.

### Legacy consumers (stale — do not mistake for a live pipeline)

These scripts hardcode `http://100.64.0.1:8088/probe` (S24) and are **NOT scheduled anywhere** (no cron, timer, or service references them; last modified 2026-09-12, before the body switch):

- `/root/scripts/forge_s24_ingest.py`
- `/root/scripts/arifs24_sensor_log.py`
- `/root/scripts/forge_reality_snapshot.py`

If any of these is ever revived, repoint it at the `.env` SOT (Honor `.6`) first. Verified 2026-10-19 14:0x MYT by 333-AGI (stabilization epoch SEAL-6c210009e58048da).
- Honor bridge process: tmux session `bridge`; repair/start: `bash ~/honor-install.sh` (phone) or the VPS copy at `/root/AAA/phone-bridge/honor-install.sh`.
- Honor battery endpoint is intermittently slow (10 s timeout observed) while `/health` stayed 200. Treat timeout as TRANSIENT, not body death: retry once, then use S24.

## 2. SSH (from the phone and from KVM8)

| Alias | Host | Address | User | Path |
|---|---|---|---|---|
| `vps` | KVM8 (af-forge) | `72.62.71.199:22888` | root | direct |
| `kvm` | KVM4 | `100.64.0.5:22` | root | Tailscale |
| `kvm2` | KVM2 (flow-edge) | `100.64.0.4:22` | root | `ProxyJump vps` |

- No KVM2 password is stored or needed; KVM8→KVM2 key path is confirmed.
- Phone key: `honor-termux` ed25519; fingerprint `SHA256:3GSzuRwQq+ZQm/LPnPMJLYIZhknD04ehBGBurrNm+Yw`; authorized on KVM8 `authorized_keys` line 42.
- Verified 2026-10-19: `ssh vps` → `forge/root`; `ssh kvm2` → `flow-edge/root`; `ssh kvm4` → `srv1946043`.

## 3. Phone UX (Arif-facing)

- One word `arif` → menu 0–7 (`~/bin/arif-menu`; aliases in `~/.bashrc`).
- `Termux:Widget` one-tap: `ARIF`, `Bridge-Health`, `SSH-VPS`, `SSH-KVM4`, `SSH-KVM2`, `Start-Bridge`.
- `Termux:Boot`: `~/.termux/boot/start-bridge` starts the bridge at boot.
- `~/.shortcuts/` holds the widget scripts.
- **Do not** ask Arif to paste long heredocs. The 2026-10-19 setup proved multi-block pastes mangle. Use the menu/widget, or a single short command sent as a Telegram code block (Copy-Paste Box Law).

## 4. Permissions / capability boundary

- Honor device info: `READ_PHONE_STATE` pending — one Android tap: Settings → Apps → Termux:API → Permissions → Phone.
- Camera / GPS / microphone: require **explicit F13 approval per use**; no standing grant.
- Sensors (magnetometer etc.) and battery are live.
- Device data is **MAP, not STORY** (human-memory compartmentalization): no personal narrative, no cross-person leakage.

## 5. Session / governance state

- Session receipt: `64fca7a2215f4c82` — **lifecycle receipt only, not a constitutional SEAL**.
- Work verdict: PARTIAL. Constitutional verdict: HOLD. No self-issued SEAL.
- VAULT999 audit 2026-10-19: 1763 ledger, 72 canonical, 959 unlinked, 2 gaps (`HASH_MISMATCH 1`, `SIGNATURE_FAIL 1`) — T3 forensic/repair HOLD.
- FQ global 0.244; 333-AGI 1.0; hermes-asi 0.244 (45 execute / 11 verify, STUCK).
- These are separate holds; the phone work does not fix them.

## 6. Agent use

- Client: `/root/AAA/phone-bridge/client.py`; env from `/root/AAA/phone-bridge/.env` (Honor) or the S24 backup.
- Read: `get_battery`, `get_device_status`, `get_sensors_snapshot`, `get_location`, `capture_camera` (approval), `show_toast`, `vibrate`.
- Act on the phone only within the authority envelope; camera/GPS/mic are F13-gated.
- If both bodies are unreachable: report `UNKNOWN`; never fabricate sensor values.

## 7. Provenance

- Evidence bundle: `/root/evidence/session-reflection-2026-10-19/` (closure receipt, reality manifest, rollback, remaining tasks, SHA256SUMS).
- Fix assets: `/root/aaa-phone/` (`ssh_config`, `arif-menu`, `shortcuts/`, `boot-start-bridge`, `bashrc-append`).
- PDF reflection: `Reflection-2026-10-19.pdf`, SHA-256 `86ad742005222f7e54fad6deaa5e0a445b0c7443633455d2a2505c19aae1f655`.

## 8. Awareness receipts

- **Hermes live surface:** `/root/.hermes/SOUL.md` section `PHONE BODY STATE — 2026-10-19`; all profile SOULs symlink to it (`aaa-hermes`, `hermes_asi`, `hermes_forge`, `hermes_apex`).
- **Hermes A2A listener** `:18089` processed this state at `2026-10-19T05:04:08Z`; task `phone-body-state-2026-10-19`; `hermes_claim_validate` PASS (confidence 0.28, structural), `hermes_contradiction_scan` PASS; `tasks_stored=1`.
- **AAA gateway** `:3001` received the broadcast as task `aaa-a66d9005-095`, but its VAULT999 seal write failed `EACCES` on `/root/.local/share/arifos/vault999/.seal_chain.lock` — gateway ack only, **not** a constitutional receipt.
- **Canonical slots:** `/root/AGENTS.md` (all coding agents), `/root/AAA/instructions/phone-body-state-2026-10-19.md` (render fragment), `/root/.local/share/arifos/carry_forward.json` (directive `e-ac4dfca7`, open loop `e-d0976ef6`), `/root/AAA/agents/AAA_STATE_MAP.md` (pointer).
- **888-APEX** acknowledged 2026-10-19: state read/recorded; VAULT999/FQ holds untouched; no mutation. **555-ASI** acknowledged 2026-10-19: read/recorded in Φ SENSE lane; no judgment, no mutation.

