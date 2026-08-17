#!/usr/bin/env python3
"""Fetch a short forecast for a city from Open-Meteo."""

import json
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

GEOCODE = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST = "https://api.open-meteo.com/v1/forecast"


def geocode(city):
    url = f"{GEOCODE}?{urlencode({'name': city, 'count': 1})}"
    with urlopen(url, timeout=15) as response:
        results = json.loads(response.read()).get("results")
    if not results:
        raise SystemExit(f"city not found: {city}")
    return results[0]["latitude"], results[0]["longitude"]


def forecast(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "forecast_days": 3,
        "timezone": "auto",
    }
    with urlopen(f"{FORECAST}?{urlencode(params)}", timeout=15) as response:
        return json.loads(response.read())


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: lookup.py <city>")
    city = sys.argv[1]
    data = forecast(*geocode(city))
    daily = data["daily"]
    for i, date in enumerate(daily["time"]):
        print(
            f"{date}: {daily['temperature_2m_min'][i]:.0f}-"
            f"{daily['temperature_2m_max'][i]:.0f} C, "
            f"{daily['precipitation_probability_max'][i]}% rain"
        )


if __name__ == "__main__":
    main()
