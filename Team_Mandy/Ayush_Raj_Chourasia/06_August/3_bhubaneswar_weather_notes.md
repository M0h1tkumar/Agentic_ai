# Bhubaneswar Weather Predictor

Before exploring the power of MCP (Model Context Protocol), we were tasked with writing a weather predictor for Bhubaneswar using a traditional API.

I implemented this in Python (`2_bhubaneswar_weather.py`) using the **Open-Meteo REST API**.

## Technical Implementation
1. **Coordinates:** Hardcoded Bhubaneswar's latitude (`20.2961`) and longitude (`85.8245`).
2. **Endpoint:** Pinged the Open-Meteo forecast API with `current_weather=true`.
3. **Parsing:** Navigated the JSON tree manually (`data["current_weather"]["temperature"]`) to extract the exact strings.

## Why this is brittle (The API problem)
If Open-Meteo changes `current_weather` to `current` in their next version, this entire script breaks. 
An AI Agent trying to use this script would fail. 
This perfectly illustrates why we need to wrap APIs in **MCP Servers**, so the LLM can dynamically read the API's schema at runtime rather than relying on hardcoded Python dict lookups!
