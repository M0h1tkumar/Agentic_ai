---
name: weather-lookup
description: Fetch the current weather forecast for a named city using Open-Meteo.
version: 1.0.0
author: Manish Prakash
---

# Weather Lookup

Returns a short weather forecast for a city.

## When to use this skill

Use it when the user asks about weather, temperature, rain, or whether they
should carry an umbrella. Do not use it for climate statistics or historical
records; this skill only covers the forecast horizon.

## Usage

Run `lookup.py` with a city name:

```bash
python3 lookup.py "Bhubaneswar"
```

## Notes

- No API key is required. Open-Meteo is free for this usage.
- The skill makes exactly one outbound request, to `api.open-meteo.com`.
- It reads no local files and writes none.
