---
name: node-device
description: Control paired mobile devices via OpenClaw node protocol. Use when: (1) Taking camera photos from paired phones, (2) Getting device location/GPS, (3) Sending notifications to paired devices, (4) Recording device screen, (5) Managing paired node connections.
---

# Node Device Skill

Control paired mobile devices (iOS/Android) via OpenClaw nodes.

## Quick Start

### List Paired Nodes

```json
{
  "tool": "nodes",
  "action": "status"
}
```

### Device Camera

```json
{
  "tool": "nodes",
  "action": "camera_snap",
  "facing": "back"
}
```

| Parameter | Description | Options |
|-----------|-------------|---------|
| `facing` | Camera to use | front, back, both |

### Device Location

```json
{
  "tool": "nodes",
  "action": "location_get",
  "desiredAccuracy": "precise"
}
```

| Parameter | Description | Options |
|-----------|-------------|---------|
| `desiredAccuracy` | GPS precision | coarse, balanced, precise |

### Send Notification

```json
{
  "tool": "nodes",
  "action": "notify",
  "title": "Alert",
  "body": "Task completed",
  "priority": "active"
}
```

| Parameter | Description | Options |
|-----------|-------------|---------|
| `title` | Notification title | string |
| `body` | Message content | string |
| `priority` | Delivery priority | passive, active, timeSensitive |
| `sound` | Sound name | string |

## Screen Recording

```json
{
  "tool": "nodes",
  "action": "screen_record",
  "durationMs": 30000
}
```

## Node Pairing

### Check Pairing Status

```bash
# Check pending pair requests
nodes action=pending

# Approve pairing
nodes action=approve requestId=<id>

# Reject pairing
nodes action=reject requestId=<id>
```

### Device Info

```json
{
  "tool": "nodes",
  "action": "device_info"
}
```

Returns:
- Device model
- OS version
- Battery level
- Storage stats
- Network status

## Use Cases

### Security / Monitoring

```json
// Periodic location check
{
  "cron": {
    "schedule": "0 */6 * * *",
    "action": "nodes location_get desiredAccuracy:balanced"
  }
}
```

### Remote Documentation

```json
// Take photo of whiteboard
{
  "nodes": {
    "action": "camera_snap",
    "facing": "back"
  }
}
```

### Alert System

```json
// Send alert on system failure
{
  "nodes": {
    "action": "notify",
    "title": "🚨 arifOS Alert",
    "body": "Disk usage > 85%",
    "priority": "timeSensitive"
  }
}
```

## Privacy & F13 (Sovereignty)

- Device control requires explicit pairing
- Location data is sensitive — encrypt logs
- Camera access: use only for legitimate documentation
- Notifications respect Do Not Disturb settings
- All actions logged to `logs/node-audit.jsonl`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Node not responding | Check network, restart companion app |
| Camera fails | Check permissions, retry |
| Location timeout | Reduce accuracy, check GPS signal |
| Pairing rejected | Regenerate pairing code, retry |
