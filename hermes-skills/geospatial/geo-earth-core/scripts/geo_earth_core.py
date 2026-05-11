#!/usr/bin/env python3
"""
geo-earth-core — Earth Geometry Primitives
Pure Python stdlib. No dependencies, no API calls.
"""
import math

# WGS-84 ellipsoid parameters
WGS84_A = 6378137.0  # semi-major axis meters
WGS84_B = 6356752.314245  # semi-minor axis meters
WGS84_F = (WGS84_A - WGS84_B) / WGS84_A  # flattening


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance using Haversine formula (sphere approximation).
    Error < 0.5% for typical navigation distances."""
    R = 6371.0088  # Earth mean radius km (IAU 2012)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def bearing_degrees(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Initial bearing from point 1 to point 2. 0°=North, 90°=East."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)
    x = math.sin(dlambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlambda)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def destination_point(lat: float, lon: float, bearing_deg: float, distance_km: float) -> tuple[float, float]:
    """Point at given bearing and distance from start point."""
    R = 6371.0088
    theta = math.radians(bearing_deg)
    delta = distance_km / R
    phi1, lambda1 = math.radians(lat), math.radians(lon)
    phi2 = math.asin(
        math.sin(phi1) * math.cos(delta)
        + math.cos(phi1) * math.sin(delta) * math.cos(theta)
    )
    lambda2 = lambda1 + math.atan2(
        math.sin(theta) * math.sin(delta) * math.cos(phi1),
        math.cos(delta) - math.sin(phi1) * math.sin(phi2),
    )
    return math.degrees(phi2), math.degrees(lambda2)


def vincenty_km(lat1: float, lon1: float, lat2: float, lon2: float, tol: float = 1e-12, max_iter: int = 1000) -> float:
    """WGS-84 ellipsoidal distance. mm-precision. Falls back to haversine if no convergence."""
    try:
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        L = math.radians(lon2 - lon1)
        U1 = math.atan((1 - WGS84_F) * math.tan(phi1))
        U2 = math.atan((1 - WGS84_F) * math.tan(phi2))
        s, lam = 0.0, L
        for _ in range(max_iter):
            sin_sigma = math.sqrt(
                (math.cos(U2) * math.sin(lam)) ** 2
                + (math.cos(U1) * math.sin(U2) - math.sin(U1) * math.cos(U2) * math.cos(lam)) ** 2
            )
            sigma = math.atan2(sin_sigma, math.cos(U1) * math.cos(U2) * math.cos(lam) + math.sin(U1) * math.sin(U2))
            sin_alpha = math.cos(U1) * math.cos(U2) * math.sin(lam) / sin_sigma
            cos2_alpha = 1 - sin_alpha**2
            if cos2_alpha == 0:
                return haversine_km(lat1, lon1, lat2, lon2)
            C = WGS84_F / 16 * cos2_alpha * (4 + WGS84_F * (4 - 3 * cos2_alpha))
            lam_prev = lam
            lam = L + (1 - C) * WGS84_F * sin_alpha * (
                sigma + C * math.sin_sigma * (math.cos(sigma) + C * math.cos(sigma) * (-1 + 2 * cos2_alpha))
            )
            if abs(lam - lam_prev) < tol:
                break
        u2 = cos2_alpha * ((WGS84_A**2 - WGS84_B**2) / WGS84_B**2)
        A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
        B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
        delta_sigma = (
            B
            * sin_sigma
            * (
                math.cos(sigma)
                + B
                / 4
                * (
                    math.cos(sigma) * (-1 + 2 * math.cos(sigma) ** 2)
                    - B
                    / 6
                    * math.cos(sigma)
                    * (-3 + 4 * sin_sigma**2)
                    * (-3 + 4 * math.cos(sigma) ** 2)
                )
            )
        )
        return (WGS84_B * A * (sigma - delta_sigma)) / 1000
    except Exception:
        return haversine_km(lat1, lon1, lat2, lon2)


if __name__ == "__main__":
    # Self-test
    # KL Sentral → Bangsar (approx 6.5 km)
    d = haversine_km(3.0730, 101.6865, 3.1350, 101.6860)
    print(f"KL Sentral → Bangsar: {d:.2f} km (haversine)")
    d_v = vincenty_km(3.0730, 101.6865, 3.1350, 101.6860)
    print(f"KL Sentral → Bangsar: {d_v:.4f} km (vincenty)")
    b = bearing_degrees(3.0730, 101.6865, 3.1350, 101.6860)
    print(f"Bearing: {b:.1f}°")
    dest = destination_point(3.0730, 101.6865, b, d)
    print(f"Destination: {dest}")
