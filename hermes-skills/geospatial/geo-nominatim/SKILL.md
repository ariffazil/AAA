---
name: geo-nominatim
description: |
  Forward and reverse geocoding via OpenStreetMap Nominatim API.
  ACTIVATES when: user asks for coordinates of an address/place, or address of coordinates.
  RATE LIMIT: 1 request/second (Nominatim policy). Always respect delay between calls.
  Requires: network access. Free, no API key.
metadata: {"openclaw": {"emoji": "📍"}, "version": "1.0.0"}
---

# geo-nominatim — OSM Nominatim Geocoding

## Trigger Conditions

- "what is the address of these coordinates"
- "lat lon of [place]"
- "where is [address/place]"
- Converting any address string to lat/lon
- Any navigation task where coordinates are needed but not provided

---

## API Endpoint

```
https://nominatim.openstreetmap.org/
```

**Headers required:**
```
User-Agent: arifOS/geo-nominatim
Accept: application/json
```

**Forward geocode:** `GET /search?q={query}&format=json&limit=1`
**Reverse geocode:** `GET /reverse?lat={lat}&lon={lon}&format=json`

---

## Rate Limiting

```python
import time
def nominatim_request(url):
    time.sleep(1.1)  # Nominatim requires max 1 req/sec
    # ... make request
```

---

## Forward Geocode Response

```json
{
  "place_id": 123456,
  "lat": "3.1180",
  "lon": "101.7170",
  "display_name": "TRX City, Kuala Lumpur, Malaysia",
  "type": "commercial_centre",
  "importance": 0.5,
  "address": {
    "city": "Kuala Lumpur",
    "state": "Wilayah Persekutuan Kuala Lumpur",
    "country": "Malaysia",
    "country_code": "my"
  }
}
```

---

## Reverse Geocode Response

```json
{
  "place_id": 234567,
  "lat": "3.1180",
  "lon": "101.7170",
  "display_name": "Tun Razak Exchange, Jalan Tun Razak, Kuala Lumpur, 50400, Malaysia",
  "address": {
    "building": "Tun Razak Exchange",
    "road": "Jalan Tun Razak",
    "city": "Kuala Lumpur",
    "postcode": "50400",
    "country": "Malaysia"
  }
}
```

---

## Python Implementation

```python
import time
import urllib.request
import urllib.parse
import json

NOMINATIM_URL = "https://nominatim.openstreetmap.org"
HEADERS = {
    "User-Agent": "arifOS/geo-nominatim",
    "Accept": "application/json"
}

def geocode(query: str, region: str = "Malaysia") -> dict | None:
    """Forward geocode: address → lat/lon."""
    q = urllib.parse.quote(f"{query}, {region}")
    url = f"{NOMINATIM_URL}/search?q={q}&format=json&limit=1&addressdetails=1"
    time.sleep(1.1)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        results = json.loads(r.read())
    if results:
        return results[0]
    return None

def reverse_geocode(lat: float, lon: float) -> dict | None:
    """Reverse geocode: lat/lon → address."""
    url = f"{NOMINATIM_URL}/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
    time.sleep(1.1)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())
```

---

## Output Format

**Forward geocode:**
```
📍 GEOCODE: "[query]"
   Lat/Lon: [lat], [lon]
   Display: [display_name]
   Type: [type]
   Importance: [0-1 score]
```

**Reverse geocode:**
```
📍 REVERSE GEOCODE: [lat], [lon]
   [display_name]
   City: [city]
   State: [state]
   Country: [country]
```

---

## Guardrails

1. **Rate limit**: Always `time.sleep(1.1)` between calls — Nominatim bans offenders
2. **No batch geocoding** without explicit user request
3. **Verify coordinates are in Malaysia** (lat: 0.8-7.5, lon: 99.5-119.5) — reject obviously bad results
4. **Confidence check**: Nominatim `importance` score < 0.1 suggests poor match
5. **Never cache results** — addresses can change; always fresh fetch
6. **User-Agent is mandatory** — Nominatim rejects missing/missingUA

---

## Common Malaysian Queries (for fallback)

| Place | Approx Lat | Approx Lon |
|-------|-----------|-----------|
| KL Sentral | 3.0730 | 101.6865 |
| TRX City | 3.1180 | 101.7170 |
| Petronas Twin Towers (KLCC) | 3.1570 | 101.7120 |
| Pavilion KL | 3.1440 | 101.7100 |
| Sunway Pyramid | 3.0730 | 101.6070 |
| Seremban | 2.7240 | 101.9380 |
| Shah Alam | 3.0730 | 101.5180 |
| Putrajaya | 2.9140 | 101.7010 |
| Cyberjaya | 2.9210 | 101.6400 |
