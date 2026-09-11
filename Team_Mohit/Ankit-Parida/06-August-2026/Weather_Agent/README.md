# Weather Prediction Agent & MCP Server Integration

This document outlines the setup, configuration, and operational workflow for the **Weather_Prediction** autonomous agent powered by the `@timlukahorstmann/mcp-weather` server and the **AccuWeather** API provider.

---

## 🎯 1. Agent Overview & Objective

- **Agent Name**: `Weather_Prediction`
- **MCP Server Package**: `@timlukahorstmann/mcp-weather`
- **Data Provider**: AccuWeather API
- **Primary Responsibility**: Provides real-time weather forecasts, temperature trends, severe weather alerts, and precipitation probability to users and downstream agent squads.

---

## ⚙ 2. MCP Server Configuration (`weather_mcp.json`)

The weather MCP server is configured via STDIO transport using `npx`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "npx",
      "args": [
        "-y",
        "@timlukahorstmann/mcp-weather"
      ],
      "env": {
        "ACCUWEATHER_API_KEY": "YOUR_KEY"
      }
    }
  }
}
```

---

## 🛠 3. Exposed MCP Tools

Upon connection, the `@timlukahorstmann/mcp-weather` server exposes the following standardized tools to the agent:

1. **`get_current_conditions`**: Fetches real-time temperature, humidity, wind speed, and weather condition text for a location.
2. **`get_5day_forecast`**: Retrieves daily high/low temperatures and conditions for the next 5 days.
3. **`get_weather_alerts`**: Checks for active severe weather warnings and advisories.

---

## 🧪 4. Sample Agent Execution & Output

### Input Query
> "What is the 5-day weather forecast for Tokyo, and are there any active weather alerts?"

### Agent Tool Invocation Trace
```json
{
  "tool": "weather_get_5day_forecast",
  "arguments": {
    "location": "Tokyo, Japan"
  }
}
```

### Response Formatted by Agent
```markdown
### ☀️ 5-Day Weather Forecast for Tokyo, Japan

| Date | Conditions | High (°C) | Low (°C) | Precipitation Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Aug 06** | Clear / Sunny | 31°C | 24°C | 10% |
| **Aug 07** | Partly Cloudy | 32°C | 25°C | 20% |
| **Aug 08** | Afternoon Showers | 29°C | 23°C | 65% |
| **Aug 09** | Clear / Sunny | 30°C | 22°C | 0% |
| **Aug 10** | Sunny | 31°C | 24°C | 5% |

**Alert Status**: 🟢 No active severe weather warnings for Tokyo.
```
