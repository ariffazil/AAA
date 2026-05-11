#!/usr/bin/env python3
"""
geo-nominatim — OSM Nominatim Geocoding Script
Forward: python geo_nominatim.py geocode "TRX City Kuala Lumpur"
Reverse: python geo_nominatim.py reverse 3.118 101.717
"""
import sys
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


def format_geocode(result: dict):
    lat = result.get("lat")
    lon = result.get("lon")
    name = result.get("display_name", "unknown")
    typ = result.get("type", "unknown")
    imp = result.get("importance", 0)
    addr = result.get("address", {})
    print(f"📍 GEOCODE RESULT")
    print(f"   Lat/Lon: {lat}, {lon}")
    print(f"   Name: {name}")
    print(f"   Type: {typ}")
    print(f"   Importance: {imp:.3f}")
    if addr:
        city = addr.get("city", addr.get("town", addr.get("village", "?")))
        state = addr.get("state", "?")
        country = addr.get("country", "?")
        postcode = addr.get("postcode", "?")
        print(f"   City: {city}")
        print(f"   State: {state}")
        print(f"   Postcode: {postcode}")
        print(f"   Country: {country}")


def format_reverse(result: dict):
    lat = result.get("lat")
    lon = result.get("lon")
    name = result.get("display_name", "unknown")
    addr = result.get("address", {})
    print(f"📍 REVERSE GEOCODE: {lat}, {lon}")
    print(f"   {name}")
    if addr:
        for key in ["building", "road", "neighbourhood", "suburb", "city", "postcode", "country"]:
            if key in addr:
                print(f"   {key}: {addr[key]}")


def main():
    if len(sys.argv) < 2:
        # Self-test
        print("=== Self-Test: TRX City ===")
        r = geocode("TRX City", "Kuala Lumpur")
        if r:
            format_geocode(r)
        return

    cmd = sys.argv[1].lower()

    if cmd == "geocode" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        print(f"🔍 Geocoding: {query}")
        r = geocode(query)
        if r:
            format_geocode(r)
        else:
            print("No results found.")
        return

    if cmd == "reverse" and len(sys.argv) >= 4:
        lat = float(sys.argv[2])
        lon = float(sys.argv[3])
        print(f"🔍 Reverse geocoding: {lat}, {lon}")
        r = reverse_geocode(lat, lon)
        if r:
            format_reverse(r)
        else:
            print("No results found.")
        return

    print("Usage:")
    print("  python geo_nominatim.py geocode 'address'")
    print("  python geo_nominatim.py reverse lat lon")


if __name__ == "__main__":
    main()
