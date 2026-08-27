# Phone Bridge — Tailscale Resolution

Phone Tailscale status check dari VPS:
- VPS Tailscale IP: 100.64.0.1 (online)
- Phone Tailscale hostname: arifs-s24 (offline, last seen 25d ago)
- Phone perlu Tailscale app running & logged in

## Options:

### A. Phone dah ada Tailscale (just restart)
Jalankan kat phone:
```
am start -a android.intent.action.MAIN -n com.tailscale.ipn/.MainActivity
```
atau buka app Tailscale kat phone, login, pastikan connected.

### B. Phone takde Tailscale lagi
Install dari Play Store / F-Droid:
- https://play.google.com/store/apps/details?id=com.tailscale.ipn
- Login dengan same Tailscale account hang VPS pakai

### C. Quick bypass — bind 0.0.0.0 (less secure, only for testing)
Set kat .env phone:
```
BRIDGE_BIND_HOST=0.0.0.0
```
Server akan listen pada semua interface (WiFi, cellular, etc).
TAPI — ini expose server ke public IP kalau hang ada port forwarding.

### D. Local network fallback (safer)
1. Check phone IP: `ip addr show wlan0` (look for 192.168.x.x)
2. Set VPS Tailscale route to phone IP, OR
3. Set VPS env `BRIDGE_PHONE_HOST=192.168.x.x`
