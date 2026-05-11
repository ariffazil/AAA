---
name: nav-kuala-lumpur
description: |
  Kuala Lumpur public transit routing — MRT Kajang/Putrajaya Lines, LRT Ampang/Kelana Jaya/Sri Petaling, KTM Komuter, Monorail.
  ACTIVATES when: any question involves navigating Kuala Lumpur public transport, MRT routes, LRT interchanges, KTM stations, or transit directions.
  Self-contained station graph with BFS routing. No internet required for routing logic.
metadata: {"openclaw": {"emoji": "🚇"}, "version": "1.0.0"}
---

# nav-kuala-lumpur — KL Transit Routing

## Trigger Conditions

- "how to get to X from Y using MRT/LRT/KTM/monorail"
- "what station is nearest to X"
- "how many stations from X to Y"
- " interchange", "换乘", "transfer" in KL context
- Questions about KL public transit lines (Kajang, Putrajaya, Ampang, Kelana Jaya, Sri Petaling, KTM, Monorail)
- "TRX", "MRT", "LRT" in KL context

---

## KL Transit Station Graph

The graph is defined in `references/kl_stations.yaml`. Each station has:
```yaml
name:        # Official station name
code:        # e.g. "SBK 08", "KJ 14", "KG 05"
lines:       # List of line codes
lat:         # Latitude WGS-84
lon:         # Longitude WGS-84
aliases:     # Alternative names people might search
```

**Line Codes:**
| Code | Line Name | Color |
|------|-----------|-------|
| SBK | MRT Kajang | Red |
| KG | MRT Putrajaya | Purple |
| PH | LRT Ampang | Grey |
| PE | LRT Kelana Jaya | Grey |
| SP | LRT Sri Petaling | Orange |
| KT | KTM Komuter | Blue |
| MO | KL Monorail | Green |

---

## Key Interchanges (Transfer Hubs)

| Station | Lines | Notes |
|---------|-------|-------|
| Muzium Negara | SBK, KG, KT | MRT Kajang ↔ MRT Putrajaya ↔ KTM |
| Pasar Senen | KG, PH, PE | MRT Putrajaya ↔ LRT Ampang ↔ LRT Kelana Jaya |
| Hang Tuah | SBK, PH, MO | MRT Kajang ↔ LRT Ampang ↔ Monorail |
| KL Sentral | SBK, KT, KLIA | MRT Kajang ↔ KTM ↔ KLIA Ekspres |
| Masjid Jamek | PH, PE | LRT Ampang ↔ LRT Kelana Jaya |
| Ampang | PH | LRT Ampang terminus |
| Sri Petaling | SBK, SP | MRT Kajang ↔ LRT Sri Petaling |
| Gombak | SBK, KT | MRT Kajang ↔ KTM |
| Kwasa Damansara | SBK, KG | MRT Kajang ↔ MRT Putrajaya |
| TRX City | SBK, KG | MRT Kajang ↔ MRT Putrajaya (underground) |

---

## Routing Algorithm

Use BFS on the station graph:

```python
def bfs_route(start_name, end_name, stations, graph):
    """Find shortest route by number of stations (transfers = line changes)."""
    from collections import deque
    
    start = find_station(start_name, stations)
    end = find_station(end_name, stations)
    if not start or not end:
        return None
    
    queue = deque([(start['name'], [start['name']])])
    visited = {start['name']}
    
    while queue:
        current, path = queue.popleft()
        if current == end['name']:
            return path
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None
```

---

## Fare Estimation

Use zone-based approximation:

```python
ZONES = {
    "Klang Valley Zone 1": ["KJ 01-13", "SP 01-08", "PH 01-08", "SBK 01-08", "KT 01-10"],
    "Klang Valley Zone 2": ["KJ 14-22", "SP 09-18", "PH 09-16", "SBK 09-35", "KT 11-20"],
}

def estimate_fare(num_stations, zone="Zone 1"):
    base = 1.00
    per_stop = 0.10
    return round(base + num_stations * per_stop, 2)
```

---

## Time Estimation

```python
def estimate_time(num_stations, has_transfer=False):
    dwell = 0.5  # min per station stop
    running = 2.0  # min per station between stops
    transfer = 5.0 if has_transfer else 0
    return round(num_stations * (dwell + running) + transfer, 1)
```

---

## Output Format for Transit Directions

```
🚇 ROUTE: [Origin] → [Destination]

Line: [Color] [Line Name]
From: [Station Name] (SBK ##)
To: [Station Name] (SBK ##)
Stops: N
Duration: ~NM minutes
 Fare: ~RM X.XX

Station sequence:
  SBK ## [Station 1]
  SBK ## [Station 2]
  ...
  SBK ## [Destination]

Transfers: N
```

---

## Trigger Examples

| User says | Interpretation |
|-----------|---------------|
| "how to go to TRX from Serdang" | MRT Kajang Line, Serdang Raya Utara → TRX City |
| "nearest MRT to Sunway" | Find nearest station to Sunway using haversine |
| "how many stops from Maluri to TRX" | BFS station count |
| "LRT to KLCC" | LRT Kelana Jaya to KLCC station |

---

## Guardrails

- Always confirm station name if ambiguous (offer alternatives)
- If station not in graph, try fuzzy match on aliases before saying "unknown"
- Always warn if service disruption is suspected (note that this is static data)
- Prefer simplest route (fewest transfers) over fastest
- When origin=destination, say so — no route needed
