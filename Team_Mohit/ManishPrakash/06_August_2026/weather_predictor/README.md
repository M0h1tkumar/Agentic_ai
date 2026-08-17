# Bhubaneswar Weather Predictor

A dependency-free Python CLI that fetches and interprets the weather forecast for
Bhubaneswar, Odisha (20.2961° N, 85.8245° E).

## Why this design

| Decision | Reason |
|---|---|
| **Open-Meteo** as the data source | No API key, no signup, no billing. Free for non-commercial use. Removes the single biggest friction point in a teaching/demo project — nobody has to hand out secrets. |
| **Stdlib only** (`urllib`, `json`, `argparse`) | Runs on any Python 3.9+ install with zero `pip install`. No supply-chain surface. |
| **Forecast, not just current conditions** | The task says *predictor*. Open-Meteo serves numerical weather-model output up to 16 days ahead, so the script genuinely predicts rather than reporting a thermometer reading. |
| **WMO code → plain English** | The API returns integer weather codes. Translating them locally keeps the output human-readable without another network call. |
| **Climate-tuned advice line** | Bhubaneswar's real risks are monsoon rain and humid heat, so the advisory logic checks rain probability, apparent temperature, and UV — not raw temperature. |

## Requirements

- Python 3.9 or newer
- An internet connection

No third-party packages. `requirements.txt` is intentionally empty.

## Usage

```bash
python3 bhubaneswar_weather.py                 # current + 3-day forecast
python3 bhubaneswar_weather.py --days 7        # week ahead
python3 bhubaneswar_weather.py --days 16       # maximum horizon
python3 bhubaneswar_weather.py --hourly        # add today's hour-by-hour table
python3 bhubaneswar_weather.py --json          # structured output for piping
```

## Sample output

```
  Bhubaneswar, Odisha — right now (07 Aug 2026, 08:15 PM IST)
  ----------------------------------------------------------
  ☁️  Overcast
      Temperature : 26.5 °C (feels like 31.7 °C)
      Humidity    : 93%
      Wind        : 11.6 km/h

  Forecast — next 2 day(s)
  ==========================================================

  ⛈️  Friday, 2026-08-07  —  Thunderstorm
      Temp        : 25.7 °C  →  30.1 °C (feels up to 36.1 °C)
      Rain        : 100% chance, 12.2 mm expected
      Wind / UV   : 11.8 km/h max, UV index 7.0
      Sun         : rises 05:23, sets 18:21
      → Carry an umbrella — rain is likely.

  ⛈️  Saturday, 2026-08-08  —  Thunderstorm
      Temp        : 25.1 °C  →  31.3 °C (feels up to 39.2 °C)
      Rain        : 99% chance, 12.0 mm expected
      Wind / UV   : 11.0 km/h max, UV index 8.9
      Sun         : rises 05:24, sets 18:20
      → Carry an umbrella — rain is likely.
```

(Captured on 7 August 2026 — peak monsoon, which is exactly what the numbers show.)

## How it maps to the MCP part of the task

The 6 August task pairs "API vs MCP" with "build a weather predictor," and that
pairing is the point. This script is the **API** half of the comparison, and it
demonstrates every drawback listed in [`../api_vs_mcp.md`](../api_vs_mcp.md):

- The endpoint, the parameter names, and the response shape are all **hard-coded**.
  If Open-Meteo renames `precipitation_probability_max`, this file breaks.
- An LLM cannot discover this tool. To let an agent use it, a developer must write
  a wrapper, a JSON schema, and a dispatch branch by hand.
- The WMO code table is a **client-side copy of server-side knowledge** — classic
  API coupling.

Wrapping the same three functions (`fetch`, `parse_days`, `describe`) behind an MCP
server would make all three problems disappear: the schema is advertised at connect
time, any MCP-speaking agent gets the tool for free, and the mapping lives with the
server. That contrast is the deliverable.

## Extending it

- **Other cities** — change `LATITUDE` / `LONGITUDE` / `CITY`, or add Open-Meteo's
  geocoding API to accept a city name argument.
- **Alerting** — pipe `--json` into `jq` and trigger on `rain_chance_pct >= 80`.
- **As an MCP tool** — expose `fetch` + `parse_days` via the `mcp` Python SDK; the
  logic is already separated from the rendering for exactly this reason.

## Source

Open-Meteo — <https://open-meteo.com> — free weather API, CC-BY 4.0 data.
