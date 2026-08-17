#!/usr/bin/env python3
"""
Bhubaneswar Weather Predictor
=============================

Fetches and summarises the weather forecast for Bhubaneswar, Odisha (India)
using the Open-Meteo forecast API.

Why Open-Meteo?
  - No API key, no signup, no rate-limit headaches for small usage.
  - Returns a proper numerical-model forecast (not just current conditions),
    so we can actually *predict* rather than merely *report*.

Usage:
    python bhubaneswar_weather.py                # 3-day forecast, table output
    python bhubaneswar_weather.py --days 7       # 7-day forecast
    python bhubaneswar_weather.py --json         # machine-readable output
    python bhubaneswar_weather.py --hourly       # today's hour-by-hour detail

Author: Manish Prakash (Team Mohit)
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

API_URL = "https://api.open-meteo.com/v1/forecast"

# Bhubaneswar, Odisha, India
CITY = "Bhubaneswar"
LATITUDE = 20.2961
LONGITUDE = 85.8245
TIMEZONE = "Asia/Kolkata"

REQUEST_TIMEOUT = 15  # seconds

# WMO weather interpretation codes -> (description, emoji)
# Reference: https://open-meteo.com/en/docs (WMO Weather interpretation codes)
WMO_CODES: dict[int, tuple[str, str]] = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Depositing rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Moderate drizzle", "🌦️"),
    55: ("Dense drizzle", "🌧️"),
    56: ("Light freezing drizzle", "🌧️"),
    57: ("Dense freezing drizzle", "🌧️"),
    61: ("Slight rain", "🌦️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    66: ("Light freezing rain", "🌧️"),
    67: ("Heavy freezing rain", "🌧️"),
    71: ("Slight snowfall", "🌨️"),
    73: ("Moderate snowfall", "🌨️"),
    75: ("Heavy snowfall", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Slight rain showers", "🌦️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Violent rain showers", "⛈️"),
    85: ("Slight snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with slight hail", "⛈️"),
    99: ("Thunderstorm with heavy hail", "⛈️"),
}


def describe(code: int) -> tuple[str, str]:
    return WMO_CODES.get(code, (f"Unknown (code {code})", "❓"))


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class DayForecast:
    date: str
    weekday: str
    condition: str
    emoji: str
    temp_max_c: float
    temp_min_c: float
    feels_like_max_c: float
    rain_chance_pct: int
    precipitation_mm: float
    wind_max_kmh: float
    uv_index_max: float
    sunrise: str
    sunset: str

    @property
    def advice(self) -> str:
        """A plain-language takeaway, tuned for Bhubaneswar's climate."""
        if self.rain_chance_pct >= 70 or self.precipitation_mm >= 10:
            return "Carry an umbrella — rain is likely."
        if self.rain_chance_pct >= 40:
            return "Rain is possible; keep an umbrella handy."
        if self.feels_like_max_c >= 42:
            return "Dangerous heat — avoid outdoor work 11am-4pm, hydrate."
        if self.feels_like_max_c >= 38:
            return "Hot and humid — stay hydrated, avoid midday sun."
        if self.uv_index_max >= 8:
            return "Very high UV — use sunscreen if outdoors."
        return "Pleasant enough; no special precautions."


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

def fetch(days: int, want_hourly: bool) -> dict[str, Any]:
    """Call the Open-Meteo forecast API and return the decoded JSON."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "timezone": TIMEZONE,
        "forecast_days": days,
        "daily": ",".join([
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "precipitation_probability_max",
            "precipitation_sum",
            "wind_speed_10m_max",
            "uv_index_max",
            "sunrise",
            "sunset",
        ]),
        "current": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "weather_code",
            "wind_speed_10m",
        ]),
    }
    if want_hourly:
        params["hourly"] = ",".join([
            "temperature_2m",
            "precipitation_probability",
            "weather_code",
        ])

    url = f"{API_URL}?{urlencode(params)}"
    try:
        with urlopen(url, timeout=REQUEST_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise SystemExit(f"Open-Meteo returned HTTP {exc.code}: {exc.reason}")
    except URLError as exc:
        raise SystemExit(f"Could not reach Open-Meteo (network problem): {exc.reason}")
    except json.JSONDecodeError:
        raise SystemExit("Open-Meteo returned a response that was not valid JSON.")


def parse_days(payload: dict[str, Any]) -> list[DayForecast]:
    daily = payload["daily"]
    out: list[DayForecast] = []
    for i, date_str in enumerate(daily["time"]):
        condition, emoji = describe(daily["weather_code"][i])
        out.append(DayForecast(
            date=date_str,
            weekday=datetime.fromisoformat(date_str).strftime("%A"),
            condition=condition,
            emoji=emoji,
            temp_max_c=daily["temperature_2m_max"][i],
            temp_min_c=daily["temperature_2m_min"][i],
            feels_like_max_c=daily["apparent_temperature_max"][i],
            rain_chance_pct=daily["precipitation_probability_max"][i] or 0,
            precipitation_mm=daily["precipitation_sum"][i] or 0.0,
            wind_max_kmh=daily["wind_speed_10m_max"][i],
            uv_index_max=daily["uv_index_max"][i],
            sunrise=daily["sunrise"][i].split("T")[1],
            sunset=daily["sunset"][i].split("T")[1],
        ))
    return out


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_current(payload: dict[str, Any]) -> None:
    current = payload.get("current")
    if not current:
        return
    condition, emoji = describe(current["weather_code"])
    observed = datetime.fromisoformat(current["time"]).strftime("%d %b %Y, %I:%M %p")

    print(f"\n  {CITY}, Odisha — right now ({observed} IST)")
    print("  " + "-" * 58)
    print(f"  {emoji}  {condition}")
    print(f"      Temperature : {current['temperature_2m']:.1f} °C "
          f"(feels like {current['apparent_temperature']:.1f} °C)")
    print(f"      Humidity    : {current['relative_humidity_2m']}%")
    print(f"      Wind        : {current['wind_speed_10m']:.1f} km/h")


def render_forecast(days: list[DayForecast]) -> None:
    print(f"\n  Forecast — next {len(days)} day(s)")
    print("  " + "=" * 58)
    for day in days:
        print(f"\n  {day.emoji}  {day.weekday}, {day.date}  —  {day.condition}")
        print(f"      Temp        : {day.temp_min_c:.1f} °C  →  {day.temp_max_c:.1f} °C "
              f"(feels up to {day.feels_like_max_c:.1f} °C)")
        print(f"      Rain        : {day.rain_chance_pct}% chance, "
              f"{day.precipitation_mm:.1f} mm expected")
        print(f"      Wind / UV   : {day.wind_max_kmh:.1f} km/h max, UV index {day.uv_index_max:.1f}")
        print(f"      Sun         : rises {day.sunrise}, sets {day.sunset}")
        print(f"      → {day.advice}")
    print()


def render_hourly(payload: dict[str, Any]) -> None:
    hourly = payload.get("hourly")
    if not hourly:
        return
    today = hourly["time"][0].split("T")[0]
    print(f"\n  Hour-by-hour for {today}")
    print("  " + "-" * 58)
    print(f"  {'Time':<8}{'Temp':<10}{'Rain':<10}Condition")
    for i, stamp in enumerate(hourly["time"]):
        date_part, time_part = stamp.split("T")
        if date_part != today:
            break
        condition, emoji = describe(hourly["weather_code"][i])
        temp = f"{hourly['temperature_2m'][i]:.1f} °C"
        rain = f"{hourly['precipitation_probability'][i]}%"
        print(f"  {time_part:<8}{temp:<10}{rain:<10}{emoji} {condition}")
    print()


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=f"Weather predictor for {CITY}, Odisha (Open-Meteo, no API key needed)."
    )
    parser.add_argument("-d", "--days", type=int, default=3,
                        help="number of forecast days, 1-16 (default: 3)")
    parser.add_argument("--hourly", action="store_true",
                        help="also show today's hour-by-hour breakdown")
    parser.add_argument("--json", action="store_true",
                        help="print raw structured output instead of a report")
    args = parser.parse_args(argv)

    if not 1 <= args.days <= 16:
        parser.error("--days must be between 1 and 16 (Open-Meteo's forecast horizon)")

    payload = fetch(args.days, args.hourly)
    days = parse_days(payload)

    if args.json:
        print(json.dumps({
            "city": CITY,
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "current": payload.get("current"),
            "forecast": [{**asdict(d), "advice": d.advice} for d in days],
        }, indent=2))
        return 0

    render_current(payload)
    render_forecast(days)
    if args.hourly:
        render_hourly(payload)
    print("  Source: Open-Meteo (open-meteo.com) — free, no API key.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
