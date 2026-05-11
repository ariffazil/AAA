---
name: geo-earth-core
description: |
  Earth ellipsoid math — great-circle distance, bearing, destination point, coordinate transforms.
  ACTIVATES when: any navigation, distance, or bearing calculation is needed.
  Pure Python stdlib. No API calls, no internet needed.
metadata: {"openclaw": {"emoji": "🌏"}, "version": "1.0.0"}
---

# geo-earth-core — Earth Geometry Primitives

Pure Python implementation of ellipsoidal geodetic calculations. No dependencies, no API calls.

## Trigger Conditions

- "how far", "distance between", "km from X to Y"
- "bearing from X to Y", "direction to"
- "what is the latitude/longitude of X" — geocoding (see geo-nominatim)
- Calculating travel distance or bearing for route analysis
- Any navigation task requiring spatial math

---

## Functions (implement in `geo-earth-core.py`)

### `haversine_km(lat1, lon1, lat2, lon2)` → float

Great-circle distance using Haversine formula (sphere approximation, error < 0.5%).

```python
import math

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth mean radius km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
```

### `bearing_degrees(lat1, lon1, lat2, lon2)` → float

Initial bearing from point 1 to point 2 (0°=North, 90°=East).

```python
def bearing_degrees(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)
    x = math.sin(dlambda) * math.cos(phi2)
    y = math.cos(phi1)*math.sin(phi2) - math.sin(phi1)*math.cos(phi2)*math.cos(dlambda)
    return (math.degrees(math.atan2(x, y)) + 360) % 360
```

### `destination_point(lat, lon, bearing_deg, distance_km)` → (lat, lon)

Point at given bearing and distance from start point.

```python
def destination_point(lat, lon, bearing_deg, distance_km):
    R = 6371.0
    theta = math.radians(bearing_deg)
    delta = distance_km / R
    phi1, lambda1 = math.radians(lat), math.radians(lon)
    phi2 = math.asin(math.sin(phi1)*math.cos(delta) + math.cos(phi1)*math.sin(delta)*math.cos(theta))
    lambda2 = lambda1 + math.atan2(math.sin(theta)*math.sin(delta)*math.cos(phi1),
                                    math.cos(delta) - math.sin(phi1)*math.sin(phi2))
    return math.degrees(phi2), math.degrees(lambda2)
```

### `vincenty_km(lat1, lon1, lat2, lon2)` → float

Ellipsoidal distance using WGS-84 (more accurate than haversine, ~mm precision). Fallback to haversine if convergence fails.

```python
def vincenty_km(lat1, lon1, lat2, lon2, tol=1e-12, max_iter=1000):
    """WGS-84 ellipsoid"""
    a, b = 6378137.0, 6356752.314245  # meters
    f = (a - b) / a
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    L = math.radians(lon2 - lon1)
    U1 = math.atan((1-f) * math.tan(phi1))
    U2 = math.atan((1-f) * math.tan(phi2))
    s, lam = 0.0, L
    for _ in range(max_iter):
        sin_sigma = math.sqrt((math.cos(U2)*math.sin(lam))**2 +
                               (math.cos(U1)*math.sin(U2) - math.sin(U1)*math.cos(U2)*math.cos(lam))**2)
        sigma = math.atan2(sin_sigma, math.cos(U1)*math.cos(U2)*math.cos(lam) + math.sin(U1)*math.sin(U2))
        sin_alpha = math.cos(U1)*math.cos(U2)*math.sin(lam) / sin_sigma
        cos2_alpha = 1 - sin_alpha**2
        if cos2_alpha == 0:
            return haversine_km(lat1, lon1, lat2, lon2)  # equatorial
        C = f/16 * cos2_alpha * (4 + f*(4 - 3*cos2_alpha))
        lam_prev = lam
        lam = L + (1-C)*f*sin_alpha*(sigma + C*math.sin_sigma*(math.cos(sigma) + C*math.cos(sigma)*(-1 + 2*math.cos(sigma)**2)))
        if abs(lam - lam_prev) < tol:
            break
    u2 = cos2_alpha * ((a**2 - b**2) / b**2)
    A = 1 + u2/16384 * (4096 + u2*(-768 + u2*(320 - 175*u2)))
    B = u2/1024 * (256 + u2*(-128 + u2*(74 - 47*u2)))
    delta_sigma = B*sin_sigma*(math.cos(sigma) + B/4*(math.cos(sigma)*(-1+2*math.cos(sigma)**2) - B/6*math.cos(sigma)*(-3+4*sin_sigma**2)*(-3+4*math.cos(sigma)**2)))
    return b * A * (sigma - delta_sigma) / 1000  # km
```

---

## Usage Pattern

```python
# Distance only
d = haversine_km(3.0730, 101.6865, 3.1350, 101.6860)  # KL Sentral to Bangsar

# Bearing
b = bearing_degrees(3.0730, 101.6865, 3.1350, 101.6860)
# 0° = North, 90° = East

# Destination
dest_lat, dest_lon = destination_point(3.0730, 101.6865, 45.0, 10.0)

# Accurate distance
d = vincenty_km(3.0730, 101.6865, 3.1350, 101.6860)
```

---

## Coordinate Reference

| City/Area | Approx Lat | Approx Lon |
|-----------|-----------|-----------|
| KL Sentral | 3.0730 | 101.6865 |
| TRX City | 3.1350 | 101.6860 |
| Serdang Raya Utara | 3.0250 | 101.7140 |
| MRT Kajang | 2.9600 | 101.7070 |

---

## Anti-Hallucination Guardrails

- Always use WGS-84 (EPSG:4326) for lat/lon
- Haversine error < 0.5% for typical navigation distances
- Vincenty is mm-accurate for WGS-84 ellipsoid
- Don't claim precision finer than the input coordinates justify
- km → miles conversion: multiply by 0.621371
